# 🚀 Specmatic Arazzo Async Demo

[Specmatic Arazzo](https://hub.docker.com/extensions/specmatic/specmatic-docker-desktop-extension) is a **NO-CODE** workflow testing tool that allows users to efficiently **author**, **validate**, **test**, and **mock** workflows, leveraging [Arazzo API Specifications](https://spec.openapis.org/arazzo/latest.html)


## 🎬 Video Walkthrough

[![Visual API Workflow Mocking and Testing with Specmatic and Arazzo API Specifications](https://img.youtube.com/vi/jrkFKh37_N0/hqdefault.jpg)](https://youtu.be/jrkFKh37_N0)


## What This Demo Shows

- **Author**, **validate**, **test**, and **mock** [**OpenAPI**](https://www.openapis.org/) and [**AsyncAPI**](https://www.asyncapi.com/) workflow with Specmatic Arazzo — without single line of code.
- Model workflows using [**Arazzo API Specifications**](https://spec.openapis.org/arazzo/latest.html) and run them via [**Specmatic Studio’s**]((https://hub.docker.com/extensions/specmatic/specmatic-docker-desktop-extension)) drag‑and‑drop UI.
- Test two microservices [**Order API**](./order_api), [**Location API**](./location_api) and exercise async messaging via [**Arazzo**](https://spec.openapis.org/arazzo/latest) with AsyncAPI over Kafka end‑to‑end.

## 🏗️ Application Architecture

This project includes below services:
- Backend Services (developed using **FastAPI**, **SQLModel**, and **SQLite**)
  - [**Order API**](./order_api)
  - [**Location API**](./location_api)
- [**Kafka Broker**](https://kafka.apache.org/)

## 🛠️ Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Specmatic Docker Extension](https://hub.docker.com/extensions/specmatic/specmatic-docker-desktop-extension)

## 🔧 Setup

### Clone the Specmatic Arazzo UI Sample repository:
```shell
git clone https://github.com/specmatic/specmatic-arazzo-async-sample
cd specmatic-arazzo-async-sample
```

### Launch the Extension:
Launch it within the Specmatic Arazzo UI Sample project directory as shown in the image below

![Specmatic Docker Extension](./assets/studio.png)

## 📝 Flow

![Diagram](./assets/flow.svg)

## Running the Project

Launch the stack by running the following docker command:
```shell
docker compose up --build
```
This builds and starts:
- [Order API](./order_api) at http://localhost:3000
- [Location API](./location_api) at http://localhost:3001
- [Kafka](https://kafka.apache.org) at localhost:9092

### Input for backend workflow testing

```json
{
    "PlaceOrder": {
        "DEFAULT": {
            "GetUserDetails": {
                "email": "specmatic@test.com",
                "password": "specmatic",
                "internalToken": "API-TOKEN"
            }
        },
        "RetrieveProducts.IsArrayEmpty": {
            "$failureMessage": "Expected not to find any products for another@user, as they belong to B Zone",
            "GetUserDetails": {
                "email": "another@user.com",
                "password": "user"
            }
        }
    }
}
```
