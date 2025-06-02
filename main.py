import json
from datetime import datetime
from decision_logic import build_behavior_tree

def run_agent_on_transaction(txn, tree, blackboard):
    # 灌入数据
    blackboard.risk_score = txn.get("risk_score", 0)
    blackboard.transaction_country = txn.get("transaction_country", "US")
    blackboard.amount = txn.get("amount", 0)
    blackboard.is_pep = txn.get("is_pep", False)

    # 执行行为树
    bt = py_trees.trees.BehaviourTree(tree)
    bt.tick()

    # 判定动作
    action = "pass"
    if blackboard.risk_score > 0.85 and blackboard.transaction_country != "US":
        action = "block"
    elif blackboard.is_pep and blackboard.amount > 10000:
        action = "flag"

    # 记录日志
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": txn.get("user_id"),
        "tx_id": txn.get("tx_id"),
        "risk_score": blackboard.risk_score,
        "country": blackboard.transaction_country,
        "amount": blackboard.amount,
        "is_pep": blackboard.is_pep,
        "action": action
    }

    return log_entry

if __name__ == "__main__":
    import py_trees

    # 构建行为树
    tree, blackboard = build_behavior_tree()

    # 示例交易数据
    sample_txns = [
        {
            "user_id": "u001",
            "tx_id": "txn1001",
            "risk_score": 0.9,
            "transaction_country": "CN",
            "amount": 12000,
            "is_pep": False
        },
        {
            "user_id": "u002",
            "tx_id": "txn1002",
            "risk_score": 0.3,
            "transaction_country": "US",
            "amount": 15000,
            "is_pep": True
        },
        {
            "user_id": "u003",
            "tx_id": "txn1003",
            "risk_score": 0.2,
            "transaction_country": "US",
            "amount": 300,
            "is_pep": False
        }
    ]

    # 执行代理
    logs = []
    for txn in sample_txns:
        log = run_agent_on_transaction(txn, tree, blackboard)
        print(f"[{log['tx_id']}] → Action: {log['action']}")
        logs.append(log)

    # 写入日志文件
    with open("logs/decision_log.json", "w") as f:
        json.dump(logs, f, indent=2)

import redis

# 连接 Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# 存入缓存
r.lpush(f"user:{user_id}:recent_tx", tx_id)

# 检查缓存长度
if r.llen(f"user:{user_id}:recent_tx") > 5:
    action = "block"  # 频繁交易行为
