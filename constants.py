# Created by SezerBozkir<admin@sezerbozkir.com> at 10/18/2020
compose_baseline = {"version": "3",
                    "services":
                        {
                        }
                    }
mysql = {
    "mysql": {
        "container_name": "sample_db",  # TODO make it dynamic
        "restart": "always",
        "image": "mysql:latest",
        "ports": [
            "3306:3306"
        ],
        "environment": {
            "MYSQL_ROOT_PASSWORD": "burayi_degistir"  # TODO make it dynamic
        },
        "volumes": [
            "/root/management/mysql/data:/var/lib/mysql"  # TODO make it dynamic
        ]
    },
    "app": {
        "depends_on": ["mysql"],
        "image": "phpmyadmin/phpmyadmin",
        "container_name": "phpmyadmin",  # TODO make it dynamic
        "restart": "always",
        "ports": ["3307:80"],
        "environment": {
            "PMA_HOST": "mysql"
        }
    }
}
