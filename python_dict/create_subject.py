import sys,statistics
sys.path.append("/dic/neo4j")

from create_node_and_relationship import CreateNodeAndRelationship as CNAR

def c(node1, node2, type, relationship):
    cnar.create_Node(node_name=node1, type=type)
    cnar.create_Node(node_name=node2, type=type)
    cnar.create_relationship(node1, node2, relationship)

def s(node1, node2, score):
    cnar.create_Node(node_name=node1)
    cnar.create_Node(node_name=node2)
    cnar.create_score(node1, node2, score)

cnar = CNAR()
relationship = "have"
c("離散数学", "論理演算の特徴", "テクノロジ系", relationship)
c("離散数学", "表現できるビットパターン数", "テクノロジ系", relationship)
c("プログラム言語", "Javaサーブレット", "テクノロジ系", relationship)
c("プロセッサ", "アドレス指定方式", "テクノロジ系", relationship)
c("プロセッサ", "投機実行の説明はどれか", "テクノロジ系", relationship)

c("プロジェクトの統合", "計画プロセスグループで実施するもの", "マネジメント系", relationship)
c("プロジェクトの時間", "所要時間を短縮する技法はどれか", "マネジメント系", relationship)
c("プロジェクトのコスト", "ファンクションポイント法", "マネジメント系", relationship)
c("プロジェクトの資源", "作業要員数の把握", "マネジメント系", relationship)
c("バーチャルサービスデスク", "サービスの運用", "マネジメント系", relationship)

c("情報システム戦略", "エンタープライズアーキテクチャ", "ストラテジ系", relationship)
c("情報システム戦略", "投資額を回収するための年間利益", "ストラテジ系", relationship)
c("業務プロセス", "BPMの目的はどれか", "ストラテジ系", relationship)
c("OR・IE", "重み付け総合評価法", "ストラテジ系", relationship)
c("OR・IE", "線形計画法", "ストラテジ系", relationship)

s("シンジ", "論理演算の特徴", "70")
s("シンジ", "表現できるビットパターン数", "40")
s("シンジ", "離散数学", str(statistics.mean([70,40])))

s("シンジ", "Javaサーブレット", "20")
s("シンジ", "Javaサーブレット", "20")








cnar.close()
# cn = CN()
# session = cn.get_session()
# session.run(CMQ._create_MATCH_query(node1_name=node1, node2_name=node2, relationship=relationship))
# cn.close()