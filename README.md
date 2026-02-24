
# Table of Contents

1.  [Project Explanation](#org0c19a12)
    1.  [Client](#org11df23b)
    2.  [Server](#orgfc5ddec)
2.  [Install and Use with Docker](#org7714d67)
    1.  [Introduction](#org6f54573)
    2.  [Prerequisites](#orgf1656a0)
    3.  [Steps](#org3845af9)
    4.  [Query the Server](#org094d481)
3.  [Install and Use with SysVinit (Debian)](#org47c6af7)
    1.  [Init Script](#org1ca1f8a)
    2.  [Control the Service](#org981ffc8)
    3.  [Logrotate](#org6c97aab)
4.  [Manual Run and Troubleshooting](#org45f8ba7)
    1.  [Run Client Manually](#orgd312bf3)
    2.  [Run Server Manually](#orgd0d219c)
    3.  [Common Issues](#org12ad1d7)
5.  [Summary](#org72c516c)



<a id="org0c19a12"></a>

# Project Explanation

This project provides a **Python-based Xtream protocol client/server
stack**. It is designed to fetch, filter, store, and serve stream
metadata for **live**, **VOD**, and **series** streams.


<a id="org11df23b"></a>

## Client

-   Authenticates against an external Xtream API using username/password.
-   Fetches metadata for all streams (live, VOD, series).
-   Filters streams based on a **whitelist** and **blacklist** of categories or names.
-   Stores filtered streams in a **SQLite database**.
-   Refreshes streams daily at a scheduled time.


<a id="orgfc5ddec"></a>

## Server

-   Exposes a REST API (/streams) to query stored streams.
-   Supports filtering by stream type (live, vod, series).
-   Requires its own username/password authentication.
-   Runs on port **8080** by default.

This setup allows you to maintain a curated set of streams locally and serve them securely to clients.


<a id="org7714d67"></a>

# Install and Use with Docker


<a id="org6f54573"></a>

## Introduction

It creates a docker container with client and server on port 8080.


<a id="orgf1656a0"></a>

## Prerequisites

-   Docker
-   make


<a id="org3845af9"></a>

## Steps

1.  Build the image:
    
        make build

2.  Run the container:
    
        make run

3.  Stop the container:
    
        make stop

4.  Other make options
    
        make image-rm # deletes docker image
        make start
        make attach


<a id="org094d481"></a>

## Query the Server

    curl -u server_user:server_pass "http://localhost:8080/streams?type=live"

This will return JSON with the filtered streams.


<a id="org47c6af7"></a>

# Install and Use with SysVinit (Debian)


<a id="org1ca1f8a"></a>

## Init Script

A single init script (/etc/init.d/xtream-app) manages both client and server.

1.  Copy the script to `/etc/init.d/xtream-app`.
2.  Make it executable:
    
        sudo chmod +x /etc/init.d/xtream-app
3.  Register with SysVinit:
    
        sudo update-rc.d xtream-app defaults


<a id="org981ffc8"></a>

## Control the Service

    sudo service xtream-app start
    sudo service xtream-app stop
    sudo service xtream-app restart
    sudo service xtream-app status


<a id="org6c97aab"></a>

## Logrotate

Logs are stored in:

-   `/var/log/xtream-client.log`
-   `/var/log/xtream-server.log`

A logrotate config (/etc/logrotate.d/xtream-app) rotates logs daily, keeps 7 days, compresses old logs, and ensures they don’t grow indefinitely.


<a id="org45f8ba7"></a>

# Manual Run and Troubleshooting


<a id="orgd312bf3"></a>

## Run Client Manually

    python client.py

This will fetch and store streams immediately.


<a id="orgd0d219c"></a>

## Run Server Manually

    python server.py

Server will start on `http://localhost:8080`.


<a id="org12ad1d7"></a>

## Common Issues

-   **Authentication errors**: Check `config.py` credentials for both client and server.
-   **Database not found**: Ensure `streams.db` exists or run `client.py` once to initialize.
-   **Port conflicts**: Change the port in `server.py` if 8080 is already in use.
-   **Logs**: Check `/var/log/xtream-client.log` and `/var/log/xtream-server.log` for runtime errors.


<a id="org72c516c"></a>

# Summary

You can run this project in three ways:

-   **Docker Compose**: Recommended for easy deployment and containerized environments.
-   **SysVinit**: For traditional service management on Debian-based systems.
-   **Manual Run**: For development, debugging, and troubleshooting.

This flexibility ensures you can deploy the Xtream client/server stack in the environment that best suits your needs.

