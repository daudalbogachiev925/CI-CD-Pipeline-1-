# CI-CD-Pipeline-1-
Описание: полноценный CI/CD: сборка, тесты, проверки, деплой на среды, откат, версионирование.


Полный pipeline для 1С: сборка, тесты, деплой на dev/test/uat/prod, откат.

## Компоненты
- Pipeline engine (stages, results)
- Environments config (YAML)
- Deploy через DESIGNER
- Rollback к предыдущему релизу
- GitHub Actions / Jenkins / GitLab CI

## Запуск
```bash
pytest -v
python -m src.deploy --env dev --cf out/cf
```
