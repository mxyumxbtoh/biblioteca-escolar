import flet as ft
import requests

API_URL = "http://127.0.0.1:8000/libros"

def obtener_icono(nombre_icono: str):
    nombre_upper = nombre_icono.upper()
    nombre_lower = nombre_icono.lower()
    if hasattr(ft, "Icons") and hasattr(ft.Icons, nombre_upper):
        return getattr(ft.Icons, nombre_upper)
    if hasattr(ft, "icons"):
        if hasattr(ft.icons, nombre_upper):
            return getattr(ft.icons, nombre_upper)
        if hasattr(ft.icons, nombre_lower):
            return getattr(ft.icons, nombre_lower)
    return None

def main(page: ft.Page):
    page.title = "Sistema de Gestión - Biblioteca Escolar"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    id_libro_edicion = {"id": None}

    txt_titulo = ft.TextField(label="Título", expand=True)
    txt_autor = ft.TextField(label="Autor", expand=True)
    txt_genero = ft.TextField(label="Género", expand=True)
    txt_anio = ft.TextField(label="Año de publicación", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    txt_ejemplares = ft.TextField(label="Ejemplares disponibles", keyboard_type=ft.KeyboardType.NUMBER, expand=True)

    def mostrar_mensaje(mensaje: str, es_error: bool = False):
        snack = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor="red700" if es_error else "green700"
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def limpiar_formulario(e=None):
        id_libro_edicion["id"] = None
        txt_titulo.value = ""
        txt_autor.value = ""
        txt_genero.value = ""
        txt_anio.value = ""
        txt_ejemplares.value = ""
        btn_guardar.text = "Guardar Libro"
        btn_guardar.icon = obtener_icono("save")
        page.update()

    def preparar_edicion(libro):
        id_libro_edicion["id"] = libro["id"]
        txt_titulo.value = str(libro.get("titulo") or "")
        txt_autor.value = str(libro.get("autor") or "")
        txt_genero.value = str(libro.get("genero") or "")
        txt_anio.value = str(libro.get("anio_publicacion") or "")
        txt_ejemplares.value = str(libro.get("ejemplares") or "")
        
        btn_guardar.text = "Actualizar Libro"
        btn_guardar.icon = obtener_icono("edit")
        mostrar_mensaje(f"Cargados datos del libro ID {libro['id']} para edición.")
        page.update()

    def solicitar_confirmacion_eliminar(libro_id):
        def confirmar_eliminacion(e):
            try:
                res = requests.delete(f"{API_URL}/{libro_id}")
                if res.status_code in (200, 204):
                    mostrar_mensaje("Libro eliminado correctamente.")
                    cargar_tabla()
                else:
                    mostrar_mensaje("No se pudo eliminar el libro.", es_error=True)
            except Exception as ex:
                mostrar_mensaje(f"Error de conexión: {str(ex)}", es_error=True)
            finally:
                dlg_confirmar.open = False
                page.update()

        def cancelar(e):
            dlg_confirmar.open = False
            page.update()

        dlg_confirmar = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Desea eliminar permanentemente el libro con ID {libro_id}?"),
            actions=[
                ft.TextButton("Eliminar", on_click=confirmar_eliminacion),
                ft.TextButton("Cancelar", on_click=cancelar),
            ],
        )
        page.dialog = dlg_confirmar
        dlg_confirmar.open = True
        page.update()

    def guardar_o_actualizar(e):
        if not txt_titulo.value or not txt_autor.value:
            mostrar_mensaje("Los campos Título y Autor son obligatorios.", es_error=True)
            return

        payload = {
            "titulo": txt_titulo.value.strip(),
            "autor": txt_autor.value.strip(),
            "genero": txt_genero.value.strip(),
            "anio_publicacion": int(txt_anio.value) if txt_anio.value.isdigit() else 0,
            "ejemplares": int(txt_ejemplares.value) if txt_ejemplares.value.isdigit() else 0
        }

        try:
            if id_libro_edicion["id"] is None:
                res = requests.post(f"{API_URL}/", json=payload)
                if res.status_code in (200, 201):
                    mostrar_mensaje("Libro creado correctamente.")
                    limpiar_formulario()
                    cargar_tabla()
                else:
                    mostrar_mensaje("Error al crear el libro.", es_error=True)
            else:
                libro_id = id_libro_edicion["id"]
                res = requests.put(f"{API_URL}/{libro_id}", json=payload)
                if res.status_code in (200, 204):
                    mostrar_mensaje("Libro actualizado correctamente.")
                    limpiar_formulario()
                    cargar_tabla()
                else:
                    mostrar_mensaje("Error al actualizar el libro.", es_error=True)
        except Exception as ex:
            mostrar_mensaje(f"Error de comunicación con la API: {str(ex)}", es_error=True)

    def cargar_tabla():
        tabla.rows.clear()
        try:
            res = requests.get(f"{API_URL}/")
            if res.status_code == 200:
                libros = res.json()
                for libro in libros:
                    tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(libro.get("id", "")))),
                                ft.DataCell(ft.Text(str(libro.get("titulo", "")))),
                                ft.DataCell(ft.Text(str(libro.get("autor", "")))),
                                ft.DataCell(ft.Text(str(libro.get("genero", "")))),
                                ft.DataCell(ft.Text(str(libro.get("anio_publicacion", "")))),
                                ft.DataCell(ft.Text(str(libro.get("ejemplares", "")))),
                                ft.DataCell(
                                    ft.Row(
                                        controls=[
                                            ft.TextButton(
                                                "Editar",
                                                icon=obtener_icono("edit"),
                                                on_click=lambda e, l=libro: preparar_edicion(l)
                                            ),
                                            ft.TextButton(
                                                "Eliminar",
                                                icon=obtener_icono("delete"),
                                                icon_color="red",
                                                on_click=lambda e, l_id=libro["id"]: solicitar_confirmacion_eliminar(l_id)
                                            ),
                                        ],
                                        spacing=5
                                    )
                                ),
                            ]
                        )
                    )
                page.update()
            else:
                mostrar_mensaje("No se pudo obtener la lista de libros.", es_error=True)
        except Exception:
            mostrar_mensaje("Error al conectar con la API backend.", es_error=True)

    btn_guardar = ft.ElevatedButton("Guardar Libro", icon=obtener_icono("save"), on_click=guardar_o_actualizar)
    btn_cancelar = ft.OutlinedButton("Cancelar / Limpiar", icon=obtener_icono("clear"), on_click=limpiar_formulario)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Título")),
            ft.DataColumn(ft.Text("Autor")),
            ft.DataColumn(ft.Text("Género")),
            ft.DataColumn(ft.Text("Año")),
            ft.DataColumn(ft.Text("Ejemplares")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    page.add(
        ft.Text("📚 Biblioteca Escolar - Módulo de Gestión", size=22, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Column(
            controls=[
                ft.Row([txt_titulo, txt_autor]),
                ft.Row([txt_genero, txt_anio, txt_ejemplares]),
                ft.Row([btn_guardar, btn_cancelar], alignment=ft.MainAxisAlignment.END),
            ],
            spacing=10
        ),
        ft.Divider(),
        ft.Text("Inventario de Libros", size=18, weight=ft.FontWeight.BOLD),
        tabla
    )

    cargar_tabla()

if __name__ == "__main__":
    ft.app(target=main)