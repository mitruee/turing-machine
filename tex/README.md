### Команда для генерации pdf:
```
docker run --rm -i -v ${PWD}:/data -v  ${PWD}/fonts:/root/.fonts mingc/latex xelatex -shell-escape main.tex
```

### Команда для сборки литературы:
```
docker run --rm -i -v ${PWD}:/data -v  ${PWD}/fonts:/root/.fonts mingc/latex biber main
```