使用者需求
================================================================================

目前只有兩種使用者：

* 考試委員
* 應聘人

應聘人到 https://exam.yueh-cake.com/jobs.at.ho600/ 頁面上，填入公錀、 14 碼驗證碼，按下「註冊系統」。 js 程式就會把 14 碼驗證碼用應聘人公錀及 jobs.at.ho600@exam.yueh-cake.com 公錀加密後，上傳至 AWS API Gateway ，再透過 AWS Lambda 函式處理，完成帳號創建步驟。

完成帳號創建後，應聘人會被轉到 https://exam.yueh-cake.com/jobs.at.ho600/<專屬帳號>-<PGP Key ID>/ 的網頁。而上述的 14 碼驗證碼加密檔會儲存至 https://exam.yueh-cake.com/jobs.at.ho600/<專屬帳號>-<PGP Key ID>/00.gpg 。

考試委員收到帳號創建通知後，就會把考題用應聘人公錀及 jobs.at.ho600@exam.yueh-cake.com 公錀加密後，上傳至 https://exam.yueh-cake.com/jobs.at.ho600/<專屬帳號>-<PGP Key ID>/01Q.gpg 。

當應聘人回到 https://exam.yueh-cake.com/jobs.at.ho600/<專屬帳號>-<PGP Key ID>/ 頁面時，就會看到信件列表：

* 00.gpg
* 01Q.gpg

點選 01Q.gpg 的連結後，即下載至個人電腦。應聘人自行在本機作 pgp 解密，完成解答後，再將「純文字的解答」貼入回答框後送出。 js 會把該「純文字解答」用應聘人公錀及 jobs.at.ho600@exam.yueh-cake.com 公錀加密後，上傳至 AWS API Gateway ，再透過 AWS Lambda 函式處理，儲存至 https://exam.yueh-cake.com/jobs.at.ho600/<專屬帳號>-<PGP Key ID>/01A.gpg 。

應聘人的網頁，此時可見到信件列表如下：

* 00.gpg
* 01Q.gpg
* 01A.gpg

而回答框會消失，改為顯示「請耐心等候回應」字句。應聘人可定時回專屬網頁確認，也可利用監控服務，定時去讀取 https://exam.yueh-cake.com/jobs.at.ho600/<專屬帳號>-<PGP Key ID>/02Q.gpg 的連結，一但有檔案可下載，監控服務可立即通知。

.. note::

    要花錢的話，可用 nodeping ，便宜又大碗，還有無限量 SMS 通知功能。要省錢的話，就自己用 Linux Crontab 跑個 wget && sendmail 來解決。

第二題至第九題的流程重覆如上，最多只會到第九題，是因為最後一題就是考試委員要求應聘人提供真實世界聯絡方式的問題，而敝司筆試最多八題。但也有可能是 01Q.gpg 內就放了多個題目，這樣問答來回的次數就會比較少。
