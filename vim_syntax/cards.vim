
" Vim syntax file
" Language: Markdown memorization cards
" Maintainer: guiferviz
" Latest Revision: January 2020

if exists("b:current_syntax")
  finish
endif

" Inside the cards, markdown syntax highlighting is going to be used.
runtime! syntax/markdown.vim
unlet! b:current_syntax


"""""""""""""""""""""""""""""""""""""""""""""
"  Keywords, regex and region definitions.  "
"""""""""""""""""""""""""""""""""""""""""""""

" Card section separators.
" cardsOutsideComment, the region defined right down is going to capture all
" the matches so no cardsSeparator is going to be highlighted outside cards.
syn match cardsSeparator /-\{3,\}/
syn match cardsSeparator /=\{3,\}/

" All text that is not inside of a card is a comment, so it's ignored
" for the card generator.
syn region cardsOutsideComment
\   start="^" end="$"
\   contains=cardBlock,cardsTodoComment

" Somewhere in syntax/markdown.vim appears "syn case ignore".
" I don't want words like: todo, fixme, xxx... to be highlighted.
syn case match
syn keyword cardsTodoComment contained TODO FIXME XXX NOTE

" Cards definition. Basically, anything between <<< and >>>.
syn region cardBlock
\   matchgroup=cardsDelimiter start="<\{3,\}" end=">\{3,\}"
\   fold contained contains=TOP,cardsOutsideComment,markdownH1

" I want to ignore the H1 made with === and the H2 made with --- to avoid
" collisions with my card separators.
syn clear markdownH1
syn clear markdownH2
" But I want to keep the syntax highlight in H1 and H2 made with # and ##.
syn region markdownH1 matchgroup=markdownHeadingDelimiter start="##\@!"      end="#*\s*$" keepend oneline contains=@markdownInline,markdownAutomaticLink contained
syn region markdownH2 matchgroup=markdownHeadingDelimiter start="###\@!"     end="#*\s*$" keepend oneline contains=@markdownInline,markdownAutomaticLink contained


"""""""""""""""""""""""""""""
"  Highlight default links  "
"""""""""""""""""""""""""""""

hi def link cardsTodoComment Todo
hi def link cardsOutsideComment Comment
hi def link cardsDelimiter Delimiter
hi def link cardsSeparator Underlined


let b:current_syntax = "cards"

