import yaml
import datetime
from ncclient import manager
from ncclient.xml_ import to_ele

CONFIG_XML = """
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <ifm xmlns="urn:huawei:yang:huawei-ifm">
      <interfaces>
        <interface>
          <name>GE0/0/0</name>
          <description>WAN</description>
        </interface>
      </interfaces>
    </ifm>
</config>
"""

NOMBRE_ARCHIVO_CFG = "colegio_001.cfg"

def huawei_connect(router):
    return manager.connect(
        host=router["host"],
        port=int(router["port"]),
        username=router["user"],
        password=router["password"],
        hostkey_verify=False,
        device_params={'name': "huaweiyang"},
        allow_agent=False,
        look_for_keys=False,
        timeout=20
    )

def push_ifm(router):
    nombre = router["nombre"]
    try:
        with huawei_connect(router) as m:
            m.edit_config(
                target="candidate",
                config=CONFIG_XML,
                error_option="rollback-on-error"
            )
            m.commit()
            print(f"[{nombre}] ✅ IFM aplicado correctamente")

            # --- Guardar en startup, para que sobreviva a un reinicio ---
            rpc = to_ele(f"""
                <save xmlns="urn:huawei:yang:huawei-cfg">
                  <filename>{NOMBRE_ARCHIVO_CFG}</filename>
                </save>
            """)
            m.dispatch(rpc)
            print(f"[{nombre}] 💾 Configuración guardada")
            return (nombre, "OK")

    except Exception as e:
        print(f"[{nombre}] ❌ Error: {e}")
        return (nombre, "FALLO")

def cargar_inventario(archivo="inventario.yml"):
    with open(archivo) as f:
        data = yaml.safe_load(f)
    return data["routers"]

if __name__ == '__main__':
    routers = cargar_inventario()
    resultados = []

    print(f"Aplicando IFM en {len(routers)} routers...\n")
    for router in routers:
        resultado = push_ifm(router)
        resultados.append(resultado)

    # --- Resumen final ---
    fallidos = [r for r in resultados if r[1] == "FALLO"]
    print(f"\n=== RESUMEN ===")
    print(f"✅ Exitosos: {len(resultados) - len(fallidos)}/{len(routers)}")
    print(f"❌ Fallidos: {len(fallidos)}")
    for nombre, estado in fallidos:
        print(f"   - {nombre}")