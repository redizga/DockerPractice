### Ubuntu_1
1. Написать код симулятора
    * Использовать класс sensor и наследников
    * Использовать переменные среды для конфигурирования
    
2. Показать настройку деплоя (через pycharm ssh)
3. Показать запуск через докер
```shell
docker build -t antonaleks/sensor-sim .
docker run -e SIM_HOST=192.168.0.114 -e SIM_TYPE=temperature --name temperature antonaleks/sensor-sim
docker push antonaleks/sensor-sim
```
4. Продемонстрировать запуск через docker-compose двух сенсоров (пример в репозитории)

### Ubuntu_2
1. Загрузить mosquitto брокер, создать mosquitto.conf файл
2. Запустить контейнер с привязкой к порту и загрузкой conf файла в систему
```shell
   docker run -v $PWD/mosquitto:/mosquitto/config -p 1883:1883 --name broker --rm eclipse-mosquitto
```
3. Проверить через mqtt explorer

### Ubuntu_3
1. influx - развернуть контейнер, указать точки монтирования
   1. Запустить контейнер с БД с приатаченным volume (версия 1.8)
   ```shell
   sudo docker run -d -p 8086:8086 -v influx:/var/lib/influxdb --name influxdb influxdb:1.8
   ```
   2. Запустить в контейнере influxdb 
   ```shell
   CREATE database sensors
   USE sensors
   CREATE USER telegraf WITH PASSWORD 'telegraf' WITH ALL PRIVILEGES
   ```
2. Telegraf - сконфигурировать как в гайде
   1. Получить конфигурационный файл
   ```shell
   sudo docker run --rm telegraf telegraf config > telegraf.conf
   ```
   2. Вставить следующую конфигурацию:
   ```shell
   # в блок mqtt_consumer
   servers = ["tcp://192.168.1.1:1883"] # адрес vm с mqtt-брокером
   topics = [
     "sensors/#"
   ]
   data_format = "value"
   data_type = "float"
   
   # в блок [outputs.influxdb]    
   urls = ["http://192.168.26.10:8086"] # адрес докера с influxdb (указать alias при docker-compose)
   database = "sensors"
   skip_database_creation = true
   username = "telegraf"
   password = "telegraf"
   ```
   3. Запустить телеграф
   ```shell
   sudo docker run  -v $PWD/telegraf:/etc/telegraf:ro -d telegraf
   ```
3. Сконфигурировать grafana через интерфейс
   1. Запустить контейнер с графаной
   ```shell
   sudo docker run --rm -d grafana/grafana
   ```
   2. Экспортировать grafana.ini на хост файл
   ```shell
   sudo docker exec -it <container_id> cat /etc/grafana/grafana.ini > grafana.ini
   ```
   3. Запустить контейнер
   ```shell
   sudo docker run -p 3000:3000 -v $PWD/grafana:/etc/grafana -v grafana-data:/var/lib/grafana  --name grafana -d grafana/grafana
   ```
   4. Сконфигурировать через веб-интерфейс доступ к influxdb. IP адрес указать виртуальной машины. Логин пароль telegraf, бд sensors
   5. Удалить контейнер и volume. Создать на хост папке в grafana/provising две папки dashboards и datasources
   В папке datasources создать default.yaml со следующим содержимым:
   ```yaml
   apiVersion: 1
   
   datasources:
     - name: InfluxDB_v1
       type: influxdb
       access: proxy
       database: site
       user: telegraf
       url: http://192.168.1.10:8086
       jsonData:
         httpMode: GET
       secureJsonData:
         password: telegraf
   ```
   
   в папке dashboards создать default.yaml
   ```yaml
   apiVersion: 1
   
   providers:
     - name: 'mqtt'
       orgId: 1
       folder: ''
       type: file
       disableDeletion: false
       editable: true
       allowUiUpdates: true
       options:
         path: /etc/grafana/provisioning/dashboards
   ```
   Также сгенерировать график в grafana вручную и скопировать json графика. Этот json залить в папку с dashboards
   
4. Сконфигурировать запуск контейнеров через docker-compose
  1. Запустить с созданием отдельной сети для докеров, при этом везде в конфигурационных файлах заменить ссылку на alias (см. docker-compose.yml)


[Исходная статья](https://coderlessons.com/articles/programmirovanie/raspberry-pi-iot-datchiki-influxdb-mqtt-i-grafana)