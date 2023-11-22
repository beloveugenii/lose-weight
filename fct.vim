" Файл подсветки синтаксиса на файлов с тренировками fcrachser

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
