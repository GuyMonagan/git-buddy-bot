MENU_STRUCTURE = {
    "repo": {
        "title": "📁 Репозиторий",
        "submenu": {
            "local_ops": {
                "title": "🛠 Создание и настройка",
                "submenu": {
                    "init": {
                        "title": "Создание репозитория",
                        "explanation": "`git init` — создаёт новый пустой Git-репозиторий в текущей папке.",
                        "command": "git init",
                    },
                    "config": {
                        "title": "Настройка Git",
                        "explanation": "`git config` — используется для настройки имени, почты и других параметров.",
                        "command": 'git config --global user.name "Имя"',
                    },
                    "clone": {
                        "title": "Клонирование проекта",
                        "explanation": "`git clone` — копирует удалённый репозиторий на ваш компьютер.",
                        "command": "git clone <url>",
                    },
                    "status": {
                        "title": "Статус изменений",
                        "explanation": "`git status` — показывает текущие изменения, которые не были закоммичены.",
                        "command": "git status",
                    },
                },
            },
            "remote_ops": {
                "title": "🌍 Обмен с GitHub",
                "submenu": {
                    "remote_add": {
                        "title": "Добавить удалённый репозиторий",
                        "explanation": "`git remote add` — связывает локальный репозиторий с удалённым.",
                        "command": "git remote add origin <url>",
                    },
                    "push": {
                        "title": "Отправить изменения",
                        "explanation": "`git push` — отправляет коммиты в удалённый репозиторий.",
                        "command": "git push origin имя_ветки",
                    },
                    "pull": {
                        "title": "Получить изменения",
                        "explanation": "`git pull` — получает и объединяет изменения с удалённого репозитория.",
                        "command": "git pull origin имя_ветки",
                    },
                    "fetch": {
                        "title": "Забрать изменения (без слияния)",
                        "explanation": "`git fetch` — скачивает изменения, но не объединяет их с текущей веткой.",
                        "command": "git fetch",
                    },
                    "push_head": {
                        "title": "Отправить текущую ветку",
                        "explanation": "`git push origin HEAD` — пушит активную ветку в origin.\n"
                                       " Очень удобно, когда ты не помнишь имя ветки (а ты не помнишь).",
                        "command": "git push origin HEAD",
                    },
                },
            },
        },
    },
    "files": {
        "title": "📂 Файлы",
        "submenu": {
            "add": {
                "title": "Добавить все файлы `git add .`",
                "explanation": "`git add .` — добавляет все изменённые файлы к следующему коммиту.",
                "command": "git add .",
            },
            "custom_add": {
                "title": "Добавить файл",
                "explanation": "Введи путь до файла, и я сделаю гит для него",
                "custom_input": True,
                "command_prefix": "git add ",
                "command_suffix": "",
                "input_prompt": "Введи имя файла (или нескольких через пробел):",
            },
            "rm": {
                "title": "Удалить файл",
                "explanation": "`git rm` — удаляет файл из проекта и отслеживания.",
                "command": "git rm имя_файла",
            },
        },
    },
    "commit": {
        "title": "✍️Коммит",
        "submenu": {
            "simple_commit": {
                "title": "Простой коммит",
                "explanation": '`git commit -m "сообщение"` — сохраняет текущие изменения с комментарием.',
                "command": 'git commit -m "сообщение"',
            },
            "custom_commit": {
                "title": "Свой коммит",
                "explanation": "Введи сообщение коммита, и я соберу команду.",
                "custom_input": True,
                "command_prefix": 'git commit -m "',
                "command_suffix": '"',
                "input_prompt": "Введи текст коммита:",
            },
        },
    },
    "branches": {
        "title": "🌿 Ветки",
        "submenu": {
            "branch": {
                "title": "Список веток",
                "explanation": "`git branch` — показывает список локальных веток.",
                "command": "git branch",
            },
            "create_branch": {
                "title": "Создать ветку",
                "explanation": "`git branch имя` — создаёт новую ветку.",
                "command": "git branch имя",
            },
            "create_from_current": {
                "title": "Создать ветку от текущей",
                "explanation": "`git checkout -b имя_ветки` — создаёт новую ветку и сразу переключается на неё.",
                "command": "git checkout -b имя_ветки",
            },
            "custom_create_branch": {
                "title": "Создать свою ветку от текущей (ввод)",
                "explanation": "Введи имя новой ветки, и я соберу команду.",
                "custom_input": True,
                "command_prefix": "git checkout -b ",
                "command_suffix": "",
                "input_prompt": "Введи имя новой ветки:",
            },
            "checkout": {
                "title": "Перейти в ветку",
                "explanation": "`git checkout` — переключает текущую ветку.",
                "command": "git checkout имя",
            },
            "delete_branch": {
                "title": "Удалить ветку",
                "explanation": "`git branch -d` — удаляет локальную ветку.",
                "command": "git branch -d имя",
            },
        },
    },
    "help": {
        "title": "📖 README",
        "explanation": "Полезная информация о работе с ботом и Git.",
        "handler": "help_handler",
    },
}
