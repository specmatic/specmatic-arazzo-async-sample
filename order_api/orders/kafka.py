import json

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


def kafka_worker(engine: Engine):
    print("Kafka worker started with config:", config)
    try:
        for message in consumer:
            print(f"{message.topic}:{message.partition}:{message.offset}: key={message.key} value={message.value}")
            order_request = validate_order_request(message.value, engine)
            if not order_request:
                continue

            order = place_order(order_request, engine)
            if not order:
                continue

            producer.send(config.KAFKA_SEND_TOPIC, value=order.model_dump(by_alias=True))
            producer.flush()
            print("Order placed:", order)
    except Exception as e:
        print("Kafka worker crashed:", e)
