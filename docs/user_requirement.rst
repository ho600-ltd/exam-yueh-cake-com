使用者需求
================================================================================

目前只有兩種使用者：

* 考試委員
* 應聘人

應聘人到 https://exam.yueh-cake.com/jobs.at.ho600/ 頁面上，填入公錀、 14 碼驗證碼(須用私錀作 clearsign)，按下「註冊系統」。 js 程式就會把 14 碼驗證碼用應聘人公錀及 jobs.at.ho600@exam.yueh-cake.com 公錀加密後，上傳至 AWS API Gateway ，再透過 AWS Lambda 函式處理，完成帳號創建步驟。

.. note::

    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA1

    12345678901234
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1

    iJwEAQECAAYFAlhfz/YACgkQFcbgJxW3fbHPKQP/d3Ev6wWV7J6jJ4jE3c8TxQjf
    jKDLgdF7lSStKbxjWmMEX18iQdZE0fXBxHgZEW86nN9/Ll6s/FhbosPwDdFA8dBN
    9DC0wzc/731woJq42P6nXa2hxrKQHgDK5dujQz1NxdkOOvAyiHkNpTUH37IOlvHf
    s9VcoGWZJ/mj1ucJPWo=
    =dBbN
    -----END PGP SIGNATURE-----

    12345678901234 實為 14 碼驗證碼，而其他部份是由私錀簽章得來。

完成帳號創建後，應聘人會被轉到 https://exam.yueh-cake.com/jobs.at.ho600/<專屬帳號>-<PGP Key ID>/ 的網頁。而上述的 14 碼驗證碼加密檔會儲存至 https://exam.yueh-cake.com/jobs.at.ho600/<專屬帳號>-<PGP Key ID>/0A.asc 。

考試委員收到帳號創建通知後，就會把考題用應聘人公錀及 jobs.at.ho600@exam.yueh-cake.com 公錀加密後，上傳至 https://exam.yueh-cake.com/jobs.at.ho600/<專屬帳號>-<PGP Key ID>/1Q.asc 。

當應聘人回到 https://exam.yueh-cake.com/jobs.at.ho600/<專屬帳號>-<PGP Key ID>/ 頁面時，就會看到信件列表：

* 0A.asc
* 1Q.asc

點選 1Q.asc 的連結後，即下載至個人電腦。應聘人自行在本機作 pgp 解密，完成解答後，再將「純文字的解答」(須用私錀作 clearsign)貼入回答框後送出。 js 會把該「純文字解答」用應聘人公錀及 jobs.at.ho600@exam.yueh-cake.com 公錀加密後，上傳至 AWS API Gateway ，再透過 AWS Lambda 函式處理，儲存至 https://exam.yueh-cake.com/jobs.at.ho600/<專屬帳號>-<PGP Key ID>/1A.asc 。

應聘人的網頁，此時可見到信件列表如下：

* 0A.asc
* 1Q.asc
* 1A.asc

而回答框會消失，改為顯示「請耐心等候回應」字句。應聘人可定時回專屬網頁確認，也可利用監控服務，定時去讀取 https://exam.yueh-cake.com/jobs.at.ho600/<專屬帳號>-<PGP Key ID>/2Q.asc 的連結，一但有檔案可下載，監控服務可立即通知。

.. note::

    要花錢的話，可用 nodeping ，便宜又大碗，還有無限量 SMS 通知功能。要省錢的話，就自己用 Linux Crontab 跑個 wget && sendmail 來解決。

第二題至第九題的流程重覆如上，最多只會到第九題，是因為最後一題就是考試委員要求應聘人提供真實世界聯絡方式的問題，而敝司筆試最多八題。但也有可能是 1Q.asc 內就放了多個題目，這樣問答來回的次數就會比較少。
