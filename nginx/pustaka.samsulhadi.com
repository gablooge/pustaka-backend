server{
        listen 80;
        server_name pustaka.samsulhadi.com;
        location / {
                proxy_pass http://localhost:9090;
        }
}
