import pyshorteners
import flet as ft
import pyperclip
import time
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def shorten_url(url: str) -> str:
    """
    сокращает ссылку используя сервис click.ru
    """
    return pyshorteners.Shortener().clckru.short(url)


def main(page: ft.Page):
    page.title = "link shortener"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    user_label = ft.Text("", color=ft.colors.WHITE, selectable=True, size=16)
    user_text = ft.TextField(
        label="Enter URL to shorten",
        hint_text="https://example.com",
        text_align=ft.TextAlign.LEFT,
        width=400,
        autofocus=True
    )

    dlg = ft.AlertDialog(
        modal=False,
        content=ft.Text("текст скопирован"),
    )

    progress_ring = ft.ProgressRing(visible=False)
        

    def get_info(e):
        url = user_text.value.strip()

        if not url:
            user_label.value = "Please enter a URL"
            page.update()
            return 
        
        progress_ring.visible = True
        user_label.value = "Processing..."
        page.update()
        
        try:
            shortened = shorten_url(url)
            user_label.value = shortened
            try:
                pyperclip.copy(shortened)
                page.open(dlg)
                time.sleep(0.35)
                page.close(dlg)
            except Exception as e:
                logging.error(f"Clipboard error: {e}")
        except Exception as e:
            logging.error(f"URL shortening error: {e}")
            user_label.value = f"Error: {str(e)}"

        finally:
            progress_ring.visible = False
            page.update()

    page.add(
        ft.Row(
            [
                user_label,
                user_text,
                
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                ft.ElevatedButton(text="shorten the link", on_click=get_info)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
    )

ft.app(target=main)