import exoscale

exo = exoscale.Exoscale()
zone = exo.compute.get_zone("ch-dk-2")
address ="194.182.189.68"
id_elastic="6b405dcd-dada-4ddc-9472-f9fe9aa4b12f"

elastic_ip = exo.compute.get_elastic_ip(zone, id=id_elastic)

security_group_web = exo.compute.get_security_group("web")

instance_back = exo.compute.create_instance(
     name="backend-todo-1",
     zone=zone,
     type=exo.compute.get_instance_type("medium"),
     template=exo.compute.get_instance_template(
            zone, "e48ee46a-5419-421d-b77e-ae6160d15780"),
     volume_size=50,
     security_groups=[security_group_web]
)

instance_front = exo.compute.create_instance(
     name="frontend-todo-1",
     zone=zone,
     type=exo.compute.get_instance_type("medium"),
     template=exo.compute.get_instance_template(
            zone, "9b3a25e6-38fe-4c63-85ae-762e475d8b9e"),
     volume_size=50,
     security_groups=[security_group_web],
     user_data="""
 runcmd:
 - sed -i s/159.100.246.82/$(hostname)/g /var/www/todo-list/assets/js/main.js
 - sed -i s/159.100.246.82/$(hostname)/g /var/www/todo-list/frontend/assets/js/main.js
""".format(
      eip=elastic_ip,
      hostname=instance_back.ipv4_address),
)

instance_back.attach_elastic_ip(elastic_ip)

