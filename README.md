
## Docker pull:
```
 docker pull liebling1225/csci_6221_group3

```

## Docker run:
```
docker run --name  modelscope  -p 7860:7860   -e  "types=removebg,changebg,repair-photo,human-cartoon"   -v /home/workspace/.cache:/mnt/workspace/.cache     -d   liebling1225/csci_6221_group3:latest
```


        
