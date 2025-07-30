MENU_STRUCTURE = {
    "repo": {
        "title": "📁 Репозиторий",
        "submenu": {
            "local_ops": {
                "title": "🛠 Локальные операции",
                "submenu": {
                    "init": {
                        "title": "Создание репозитория",
                        "explanation": "`git init` — создаёт новый пустой Git-репозиторий в текущей папке.",
                        "command": "git init"
                    },
                    "config": {
                        "title": "Настройка Git",
                        "explanation": "`git config` — используется для настройки имени, почты и других параметров.",
                        "command": "git config --global user.name \"Имя\""
                    },
                    "clone": {
                        "title": "Клонирование проекта",
                        "explanation": "`git clone` — копирует удалённый репозиторий на ваш компьютер.",
                        "command": "git clone <url>"
                    },
                    "status": {
                        "title": "Статус изменений",
                        "explanation": "`git status` — показывает текущие изменения, которые не были закоммичены.",
                        "command": "git status"
                    }
                }
            },
            "remote_ops": {
                "title": "🌍 Обмен с GitHub",
                "submenu": {
                    "remote_add": {
                        "title": "Добавить удалённый репозиторий",
                        "explanation": "`git remote add` — связывает локальный репозиторий с удалённым.",
                        "command": "git remote add origin <url>"
                    },
                    "push": {
                        "title": "Отправить изменения",
                        "explanation": "`git push` — отправляет ваши коммиты в удалённый репозиторий.",
                        "command": "git push origin main"
                    },
                    "pull": {
                        "title": "Получить изменения",
                        "explanation": "`git pull` — получает и объединяет изменения с удалённого репозитория.",
                        "command": "git pull origin main"
                    },
                    "fetch": {
                        "title": "Забрать изменения (без слияния)",
                        "explanation": "`git fetch` — скачивает изменения, но не объединяет их с текущей веткой.",
                        "command": "git fetch"
                    }
                }
            }
        }
    }
}
