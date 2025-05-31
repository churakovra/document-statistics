import pandas
import requests
import streamlit
from starlette.status import HTTP_200_OK

from app.config.preferences import BACKEND_PORT, BACK_SERVICE_NAME

API_URL = f"http://{BACK_SERVICE_NAME}:{BACKEND_PORT}"
PAGE_SIZE = 50

streamlit.set_page_config(
    page_title="Загрузка файла",
    layout="wide"
)

if "file_id" not in streamlit.session_state:
    streamlit.session_state.file_id = None
if "page" not in streamlit.session_state:
    streamlit.session_state.page = 0

streamlit.title("Получить статистику слов")
streamlit.write("Загрузите файл чтобы получить статистику")

uploaded_file = streamlit.file_uploader("Выберите текстовый файл", type=['txt'])

if uploaded_file is not None and streamlit.session_state.file_id is None:
    streamlit.write(f"Имя файла: {uploaded_file.name}")
    files = {"file": (uploaded_file.name, uploaded_file, "text/plain")}
    response = requests.post(f"{API_URL}/file/new", files=files)

    if response.status_code == HTTP_200_OK:
        streamlit.success(response.status_code)
        streamlit.session_state.file_id = response.json()["file_id"]
        streamlit.session_state.page = 0
    else:
        streamlit.error("Ошибка в обработке файла")

if streamlit.session_state.file_id:
    offset = streamlit.session_state.page * PAGE_SIZE
    stats_response = requests.get(
        f"{API_URL}/file",
        params={"file_id": streamlit.session_state.file_id, "size": PAGE_SIZE, "offset": offset}
    )

    if stats_response.status_code == 200:
        stats: list[dict[str: str | float]] = [
            {
                "word": row["word"],
                "tf": round(row["tf"], 5),
                "idf": round(row["idf"], 5),
            }
            for row in stats_response.json()
        ]

        df = pandas.DataFrame(stats)

        streamlit.subheader("Статистика слов")
        streamlit.dataframe(df, use_container_width=True)

        col1, col2, col3 = streamlit.columns(3)
        with col1:
            if streamlit.button("← Предыдущая", disabled=streamlit.session_state.page == 0):
                streamlit.session_state.page -= 1
        with col2:
            streamlit.write(f"Страница {streamlit.session_state.page + 1}")
        with col3:
            if len(df) == PAGE_SIZE:
                if streamlit.button("Следующая →"):
                    streamlit.session_state.page += 1

        csv = df.to_csv(index=False).encode('utf-8')
        streamlit.download_button(
            label="Выгрузить статистику в .csv формате",
            data=csv,
            file_name=f"{uploaded_file.name}_statistics.csv",
            mime="text/csv"
        )
    else:
        streamlit.error("Ошибка в получении статистики")
