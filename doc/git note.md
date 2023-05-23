* 讓git開始追蹤該資料夾: `git init`
* 新增一個檔案(叫welcome.html): `echo "hello, git" > welcome.html`
* 新增一個檔案(叫welcome.html): `git add [welcome.html]`
    1. 當使用 git add 把檔案加入至暫存區，Git 會根據這個物件的「內容」計算出 SHA-1 值。 
    2. Git 接著會用這個 SHA-1 值的前兩個字當做目錄名稱，後 38 個字當做檔案名稱，把目錄及檔案建立並存放在 .git/objects 目錄下。
    3. 那個檔案的內容則是 Git 使用壓縮演算法，把原本的「內容」壓縮之後的結果。
* check git 追蹤狀態: `git status`
* check git 歷史提交資訊: `git log`
* commit: `git commit -m 'change name'`
* 不新增commit, 把檔案加到最後一次的commit就好: `git commit --amend`
* 找一下程式是誰寫的: `git blame welcome.html`
* 如果檔案被誤刪＆還沒commit, 可以救回來的: `git checkout welcome.html`
* 將版本往前指向特定commit: `git reset [版號]` or `git reset HEAD~2`(當前HEAD往前兩個)
* 看一下git所有的編輯紀錄: `git reflog`

* 新增branch : `git branch [branch name]`
* 切換到branch : `git checkout [branch name]`

