# tcp_port_exporter
A TCP Ports Monitor Exporter for Prometheus.
```
tcp_port_exporter/
├── grafana
│   └── TCP\ Ports\ Monitor-1524464207634.json # Grafana Dashboard Json
├── README.md  # 使用说明
├── requirements.txt # 依赖包
├── rules
│   └── check_tcp_port.rules  # 告警规则
├── systemd
│   └── tcp_port_exporter.service  # 以systemd方式运行exporter
├── src
     ├── check_tcp_port.list  # 监控目标文件
     └── tcp_port_exporter.py # 主程序

```



## Usage

- cd `tcp_port_exporter/v1`
- Create a `check_tcp_port.list` file if not exists; add the targets like this format `hostname--192.168.111.111:9100` what u want to monitor;
- Run `nohup python ./tcp_port_exporter.py >> ./tcp_port_exporter.log 2>&1 &`
- Go to http://your_ip:1990/metrics to see metrics

Alternatively, if you don't wish to install the package, run using `$ vmware_exporter/vmware_exporter.py`

### Configuration

add the following config parameters to `prometheus.yml`:

```
   - job_name: 'tcp_port_exporter'
    metrics_path: /metrics
    scrape_interval: 60s
    file_sd_configs:
      - files: ['/path/to/file/check_tcp_port.json']

```

the `check_tcp_port.json` is like that:
```
[
    {
        "targets": [
            "your_ip:1990"
        ],
        "labels": {}
    }
]
```


## Metrics
```
# HELP check_tcp_port # 端口存活监测
# TYPE check_tcp_port gauge
check_tcp_port{host="192.168.111.111",port="9100"} 1.0
```

## References

The exporter uses theses libraries:
- Prometheus [client_python](https://github.com/prometheus/client_python) for Prometheus supervision

