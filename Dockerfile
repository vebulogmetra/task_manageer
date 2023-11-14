FROM python:3.10-slim

# Включает обработку ошибок Python
ENV PYTHONFAULTHANDLER=1 \
  # Запрещает Python буферизировать stdout и stderr
  PYTHONUNBUFFERED=1 \
  # Запрещает Python записывать файлы pyc на диск
  PYTHONDONTWRITEBYTECODE=1 \
  # Используется для обеспечения предсказуемости порядка элементов в хэш-таблицах
  PYTHONHASHSEED=random \
  # Отключает кэширование пакетов pip
  PIP_NO_CACHE_DIR=off \
  # Отключает проверку версии pip при использовании
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.6.1 \
  TZ=Europe/Moscow

RUN pip install "poetry==$POETRY_VERSION" \
  && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /task_mngr_app
COPY poetry.lock pyproject.toml /task_mngr_app/

RUN poetry config virtualenvs.create false \
  && poetry install --without dev --no-interaction --no-ansi

COPY . /task_mngr_app

CMD ["python", "."]

EXPOSE 8000