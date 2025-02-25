# OkatadukeClub
本システムは、Raspberry Pi（以下、ラズパイ）とサーバを連携させ、ラズパイに接続されたカメラで定期的に写真を撮影し、机の汚さを評価するサービスを提供します。
## 要件定義

- [機能要求定義書 / Fuctional Requirements](Document/FunctionalRequirements.md)
- [ドメインモデル / Domain Model](Document/DomainModel.png)
- [ユースケース図 / Use Case Diagram](Document/UseCase/UseCase.png)
- [ユースケースに関する文章 / Doucument about Use Case](Document/UseCase/UseCase.md)

## 設計

- ロバストネス図 / Robustness Diagram
  - [写真撮影とデータ送信](Document/Robustness/CapturePhoto.png)
  - [写真判定処理](Document/Robustness/JudgePhoto.png)
  - [通知送信](Document/Robustness/Notification.png)
- シーケンス図 / Sequence Diagram
  - [写真撮影とデータ送信](Document/Sequence/CapturePhoto.png) 
  - [写真判定処理](Document/Sequence/JudgePhoto.png)
  - [通知送信](Document/Sequence/Notification.png)
- [クラス図 / Class Diagram](Document/Class.png)