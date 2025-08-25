import json
import time

from kafka import KafkaConsumer, KafkaProducer
from sqlalchemy import Engine
from sqlmodel import Session, select

from order_api.config import Config
from order_api.models import Order, OrderBase, OrderPublic, Product

config = Config()  # pyright: ignore[reportCallIssue]
producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_BROKER_URI,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

consumer = KafkaConsumer(
    config.KAFKA_RECEIVE_TOPIC,
    bootstrap_servers=config.KAFKA_BROKER_URI,
    group_id=config.KAFKA_GROUP_ID,
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

def extract_correlation_id(message) -> str | None:
    if message.headers:
        for key, value in message.headers:
            if key == "orderRequestId":
                return value.decode("utf-8") if value else None
    return None

def validate_product_information(product_id: int, quantity: int, engine: Engine):
    with Session(engine) as session:
        product_exists = session.exec(select(Product).where(Product.product_id == product_id)).first()
    if not product_exists:
        msg = f"Product with id {product_id} not found"
        raise Exception(msg)
    if product_exists.quantity < quantity:
        msg = f"Product with id {product_id} is out of stock"
        raise Exception(msg)


def validate_order_request(order_request: dict, engine: Engine) -> OrderBase | None:
    try:
        order = OrderBase.model_validate(order_request)
        validate_product_information(order.product_id, order.quantity, engine)
    except Exception as e:
        print("Invalid Order Request, skipping:", e)
        return None
    else:
        return order


def place_order(order_request: OrderBase, engine: Engine) -> OrderPublic | None:
    try:
        db_order = Order.model_validate(order_request)
        with Session(engine) as session:
            session.add(db_order)
            session.commit()
            session.refresh(db_order)
        return OrderPublic.model_validate(db_order)
    except Exception as e:
        print("Invalid Order Request, skipping:", e)
        return None

def process_message(message, engine):
    print(f"{message.topic}:{message.partition}:{message.offset}: key={message.key} value={message.value}, headers={message.headers}")
    correlation_id = extract_correlation_id(message)
    if not correlation_id:
        print("Missing correlationId in request, skipping")
        return None

    order_request = validate_order_request(message.value, engine)
    if not order_request:
        return None

    order = place_order(order_request, engine)
    if not order:
        return None

    response_headers = [("orderResponseId", correlation_id.encode("utf-8"))]
    producer.send(config.KAFKA_SEND_TOPIC, value=order.model_dump(by_alias=True), headers=response_headers)
    producer.flush()
    print("Order placed:", order, " with correlationId:", correlation_id)
    return order

def kafka_worker(engine):
    print("Kafka worker started with config:", config)
    while True:
        try:
            for message in consumer:
                process_message(message, engine)
        except Exception as e:
            print("Kafka worker crashed:", e)
            time.sleep(5)
