
# Table of Contents

1.  [Project Explanation](#orgd33180b)
    1.  [Client](#orgb63afbb)
    2.  [Server](#orge3a406c)
2.  [Install and Use with Docker Compose](#orgc6ab417)
    1.  [Prerequisites](#org580b457)
    2.  [Steps](#org75e3307)
    3.  [Query the Server](#org0c897e2)
    4.  [Extra: Makefile](#org3f05462)
3.  [Install and Use with SysVinit (Debian)](#org5ff68b2)
    1.  [Init Script](#org56103e7)
    2.  [Control the Service](#org20cfbd3)
    3.  [Logrotate](#org69e9aff)
4.  [Manual Run and Troubleshooting](#orgdd8127b)
    1.  [Run Client Manually](#org5f52455)
    2.  [Run Server Manually](#org577c856)
    3.  [Common Issues](#orgf7c94ad)
5.  [Summary](#org7ffc1fb)



<a id="orgd33180b"></a>

# Project Explanation

This project provides a **Python-based Xtream protocol client/server
stack**. It is designed to fetch, filter, store, and serve stream
metadata for **live**, **VOD**, and **series** streams.


<a id="orgb63afbb"></a>

## Client

-   Authenticates against an external Xtream API using username/password.
-   Fetches metadata for all streams (live, VOD, series).
-   Filters streams based on a **whitelist** and **blacklist** of categories or names.
-   Stores filtered streams in a **SQLite database**.
-   Refreshes streams daily at a scheduled time.


<a id="orge3a406c"></a>

## Server

-   Exposes a REST API (/streams) to query stored streams.
-   Supports filtering by stream type (live, vod, series).
-   Requires its own username/password authentication.
-   Runs on port **8080** by default.

This setup allows you to maintain a curated set of streams locally and serve them securely to clients.


<a id="orgc6ab417"></a>

# Install and Use with Docker Compose


<a id="org580b457"></a>

## Prerequisites

-   Docker
-   Docker Compose


<a id="org75e3307"></a>

## Steps

1.  Build and start the stack:
    
        docker-compose up --build -d

2.  Check logs:
    
        docker-compose logs -f xtream-client
        docker-compose logs -f xtream-server

3.  Stop the stack:
    
        docker-compose down


<a id="org0c897e2"></a>

## Query the Server

    curl -u server_user:server_pass "http://localhost:8080/streams?type=live"

This will return JSON with the filtered streams.


<a id="org3f05462"></a>

## Extra: Makefile

Usage: 

1.  Build images
    
        make build
2.  Start client + server stack
    
        make up
3.  Stop everything
    
        make down
4.  Follow logs
    
        make logs
5.  Run client manually (one-off refresh)
    
        make client
6.  Run server manually
    
        make server
7.  Deletes SQLite file
    
        make delete-db

Note: after running you should run:

    make client


<a id="org5ff68b2"></a>

# Install and Use with SysVinit (Debian)


<a id="org56103e7"></a>

## Init Script

A single init script (/etc/init.d/xtream-app) manages both client and server.

1.  Copy the script to `/etc/init.d/xtream-app`.
2.  Make it executable:
    
        sudo chmod +x /etc/init.d/xtream-app
3.  Register with SysVinit:
    
        sudo update-rc.d xtream-app defaults


<a id="org20cfbd3"></a>

## Control the Service

    sudo service xtream-app start
    sudo service xtream-app stop
    sudo service xtream-app restart
    sudo service xtream-app status


<a id="org69e9aff"></a>

## Logrotate

Logs are stored in:

-   `/var/log/xtream-client.log`
-   `/var/log/xtream-server.log`

A logrotate config (/etc/logrotate.d/xtream-app) rotates logs daily, keeps 7 days, compresses old logs, and ensures they don’t grow indefinitely.


<a id="orgdd8127b"></a>

# Manual Run and Troubleshooting


<a id="org5f52455"></a>

## Run Client Manually

    python client.py

This will fetch and store streams immediately.


<a id="org577c856"></a>

## Run Server Manually

    python server.py

Server will start on `http://localhost:8080`.


<a id="orgf7c94ad"></a>

## Common Issues

-   **Authentication errors**: Check `config.py` credentials for both client and server.
-   **Database not found**: Ensure `streams.db` exists or run `client.py` once to initialize.
-   **Port conflicts**: Change the port in `server.py` if 8080 is already in use.
-   **Logs**: Check `/var/log/xtream-client.log` and `/var/log/xtream-server.log` for runtime errors.


<a id="org7ffc1fb"></a>

# Summary

You can run this project in three ways:

-   **Docker Compose**: Recommended for easy deployment and containerized environments.
-   **SysVinit**: For traditional service management on Debian-based systems.
-   **Manual Run**: For development, debugging, and troubleshooting.

This flexibility ensures you can deploy the Xtream client/server stack in the environment that best suits your needs.

