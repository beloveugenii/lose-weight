" Файл подсветки синтаксиса на файлов с тренировками simple-sport
" Поместите его в каталог '$HOME/.vim/syntax'
" Внесите в файл '$HOME/.vimrc' следующую стоку:
" au BufRead,BufNewFile *.tss set filetype=tss

" Названия параметров тренировки
syn keyword Keyword name pause repeats relax on_end
" Параметры тренировки
syn match Character /=\@<=.\+/

" Комментарии
syn match Comment /^#.\+$/

" Продолжительность выполнения упражнения
syn match Character /:\@<=.\+/
syn match Character /\(->\)\@<=.\+/

" Названия упражнений
syn match String /.\+\(:\)\@=/
syn match String /.\+\(\(->\)\)\@=/
