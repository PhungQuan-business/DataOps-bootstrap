Cần 4 servers/vms với cấu hình như sau:

- sever 1: airbyte (8Gb 2 core)
- server 2: database + airflow (12Gb 6 core 100GB storage)
- server 3: superset (8GB 2 core)
- server 4: server thao tác, dùng để thao tác với các dịch vụ

airbyte cần 8Gb và 2 core (1 máy)

superset cần tối thiểu 8GB và 2 core (1 máy)

database + airflow (1 máy 6 core 12GB 100GB)

- airflow cần 4GB và 2 core ()
- postgres + pgAdmin: 2 core 4GB 50GB storage HDD/SDD
- minio: 2 GB 2 core 50Gb storage HDD/

Giới thiệu về mục tiêu
Giới thiệu về quy trình
Giới thiệu về cài đặt

Trình bày kiến trúc tổng quát
sau đó trọng tâm vào DataOps, cho phần MLOps lại

Tài liệu cài airbyte(done)
Tài liệu cài airflow(cần chỉnh sửa)
Tài liệu cài superset()
Tài liệu cài database (90%, sửa lại ảnh là ok)
Tài liệu cài datalake (chưa có)

Tài liệu cài đặt mlflow
Tài liệu setup PySpark
