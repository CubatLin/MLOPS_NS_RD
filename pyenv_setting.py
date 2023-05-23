'''這個檔案是將一些預設pyenv的指令複製到zshrc裡面'''
import os

# 參考資料：
# >> https://blog.csdn.net/toopoo/article/details/104746623
# >> https://stackoverflow.com/questions/41129504/pycharm-with-pyenv
#
############################################################################################
os.system("echo 'export PYENV_ROOT=\"$HOME/.pyenv\"' >> ~/.zshrc") # 沒事別執行
os.system("echo 'export PATH=\"$PYENV_ROOT/shims:$PATH\"' >> ~/.zshrc") # 沒事別執行
os.system("echo 'if which pyenv-virtualenv-init > /dev/null; then eval \"$(pyenv virtualenv-init -)\"; fi' >> ~/.zshrc") # 沒事別執行
