execute scirpt by web
=====================

更新后启动
----------

- nginx配置

.. code::

    server {
        listen 80;
        listen 443 ssl;

        server_name  your-domain;

        location / {
            try_files $uri @backend;
        }

        location @backend {
            include uwsgi_params;
            uwsgi_pass unix:/tmp/auto-deploy.sock;
        }
    }

- supervisor配置

.. code::

    [program:auto-deploy]
    command=uwsgi --ini /path/uwsgi.ini
    autostart=true
