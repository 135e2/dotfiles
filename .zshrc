# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi


### Added by Zinit's installer
if [[ ! -f $HOME/.zinit/bin/zinit.zsh ]]; then
    print -P "%F{33}▓▒░ %F{220}Installing %F{33}DHARMA%F{220} Initiative Plugin Manager (%F{33}zdharma/zinit%F{220})…%f"
    command mkdir -p "$HOME/.zinit" && command chmod g-rwX "$HOME/.zinit"
    command git clone https://github.com/zdharma-continuum/zinit "$HOME/.zinit/bin" && \
        print -P "%F{33}▓▒░ %F{34}Installation successful.%f%b" || \
        print -P "%F{160}▓▒░ The clone has failed.%f%b"
fi

source "$HOME/.zinit/bin/zinit.zsh"
autoload -Uz _zinit
(( ${+_comps} )) && _comps[zinit]=_zinit

# Load a few important annexes, without Turbo
# (this is currently required for annexes)
zinit light-mode for \
    zdharma-continuum/z-a-rust \
    zdharma-continuum/z-a-as-monitor \
    zdharma-continuum/z-a-patch-dl \
    zdharma-continuum/z-a-bin-gem-node

### End of Zinit's installer chunk

# Highlighting
zinit ice lucid wait='0' atinit='zpcompinit'
zinit light zsh-users/zsh-syntax-highlighting

# Completions
zinit ice lucid wait='0'
zinit light zsh-users/zsh-completions

# Powerlevel10k
zinit ice depth=1
zinit light romkatv/powerlevel10k

# Zprof
zmodload zsh/zprof

# Load from oh-my-zsh
zinit wait="1" lucid for \
    OMZL::clipboard.zsh \
    OMZL::git.zsh \
    OMZL::history.zsh \
    OMZP::systemd/systemd.plugin.zsh \
    OMZP::sudo/sudo.plugin.zsh \
    OMZP::git/git.plugin.zsh
# Auto suggestions
zinit ice lucid wait='0' atload='_zsh_autosuggest_start'
zinit light zsh-users/zsh-autosuggestions

# Easier navigation: .., ..., ...., ....., ~ and -
# Copied from https://github.com/mathiasbynens/dotfiles/blob/main/.aliases
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."
alias ~="cd ~" # `cd` is probably faster to type though
alias -- -="cd -"

# Use exa instead
DISABLE_LS_COLORS=true
alias ls=exa

# Use batcat as cat
alias cat=batcat

# Goproxy
export GOPROXY=https://goproxy.io,direct

# Go bin
export PATH="$PATH:${HOME}/go/bin"

# GnuPG magic for commit signing
export GPG_TTY=${_P9K_TTY}

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# local PATH
export PATH="$PATH:${HOME}/.local/bin"
export PATH="$HOME/.poetry/bin:$PATH"

# Scaleway CLI autocomplete initialization.
eval "$(scw autocomplete script shell=zsh)"
