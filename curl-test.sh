#!/bin/bash

# GET
curl http://127.0.0.1:5000/api/timeline_post 

# POST
curl -X POST http://127.0.0.1:5000/api/timeline_post -d 'name=User&email=user@mlh.io&content=Added from bash script'

# GET
curl http://127.0.0.1:5000/api/timeline_post 

# DELETE
curl -X DELETE http://127.0.0.1:5000/api/timeline_post -d 'name=User' 

# GET
curl http://127.0.0.1:5000/api/timeline_post 
