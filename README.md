# Energy Management System

## Programming Task

Design and implement a RESTful Energy Management API that allows standard users to view

## Time Guidance

This exercise is scoped to ~2–3 hours of focused work. Do not over‐engineer; polish what
you have time for and document trade‐offs.
If you have a public repository that showcases your coding style—particularly in Python—feel
free to share the GitHub link along with your completed task.
Good luck – we look forward to reading your code! 🚀

## Problem Statement

You are building a minimal back‐end for an energy management system. The core domain
object is a Site. Each Site has several Devices (batteries, inverters, PV panels, wind turbines
...), and every Device reports at least one metric (e.g. battery state‐of‐charge, PV power, wind
speed).
Your goal is to expose a set of HTTP endpoints that satisfy the functional requirements below
and to provide automated tests that prove the behaviour.

## Functional Requirements

1. Site catalogue – Standard users can list and
   inspect the Sites they are authorised to see.
2. Device CRUD – Technicians can create /
   update / delete devices under any Site they
   are assigned to; standard users have
   read‐only access.

3. Metric feed – Every Device exposes at least
   one metric; the API must return the latest
   value together with metadata (timestamp,

unit).

4. Metric subscription – A user can create a
   subscription that references an arbitrary set
   of metrics (across multiple sites and devices).
5. Time‐series endpoint – The system returns a
   mocked list of numbers that represents the
   subscribed metric history for the requested
   time window.

6. Persistence – All data are stored in a
   relational database (SQLite, PostgreSQL or
   similar).

7. Tests – Provide unit/integration tests that
   cover the behaviour you consider critical.

## Optional Enhancements (nice‐to‐have)

1. Authentication & Authorisation (e.g. JWT, session cookies).
2. Server‐side rendered HTML pages for manually exploring Sites/Devices.
3. Dockerisation – 1‐click setup via `docker compose up`.
   Feel free to implement any (or none) of these if you have spare time; they will be considered a
   bonus.

## Non‐Functional Expectations

● Clean code & project structure – favour readability over micro‐optimisations.
● Documentation – briefly explain design decisions and how to run the project.
● Automated tests – green on `pytest` / `npm test` / etc.
● API description – OpenAPI/Swagger or equivalent is appreciated.

## Deliverables

1. Source code and this `README.md` (update if you deviate from the spec).
2. Test suite demonstrating the behaviour.
3. (Optional) `docker-compose.yml`, migration scripts, seed data.
   Submit a link to a public Git repository (GitHub / GitLab / Bitbucket) or a zipped archive.

# Solution

This repository is work in progress aiming to demonstrate principles of solution throughout the whole stack.

## Done

### CI/CD

Application is packed in Docker container with defined `docker-compose.yaml` using official PostgreSQL as database and nginx as production proxy.

### Schema

Core of facility (the application itself - module containing sites and devices) and auth is defined in SQL as alembic migration with model layer of corresponding classes for application usage.

### Application structure

The application is structured in two dimensions 'horizontally' in modules taking care of separate business matters. Those are not strictly divided, for example authentication supports other modules. 'Vertical' division separates code into layers with their own general purpose:

- presentation: definition of routes, validation of requests, redirection, etc.
- application: decides how the request will be handled
- infrastructure: takes care of any data manipulation
- model: Data abstraction for application usage

## TODO

- finish PostgreSQL configuration and automatic migrations
- define CI/CD pipelines building system, doing static checks and running tests
- integration testing
- apply auth module to verify user and decide access
- metric subscription
- templates and flash messages
- use more fitting database for metrics history (like ClickHouse)
