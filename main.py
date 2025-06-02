import json
from datetime import datetime
import py_trees
from decision_logic import build_behavior_tree

# ✅ 模拟 Redis 缓存：每个用户的最近交易（NoSQL-style）
transaction_cache = {}

def run_agent_on_transaction(txn, tree, blackboard):
    # 灌入黑板数据
    blackboard.risk_score = txn.get("risk_score", 0)
    blackboard.transaction_country = txn.get("transaction_country", "US")
    blackboard.amount = txn.get("amount", 0)
    blackboard.is_pep = txn.get("is_pep", False)

    # 行为树执行
    bt = py_trees.trees.BehaviourTree(tree)
    bt.tick()

    # 身份治理
    user_id = txn["user_id"]
    user_role = txn.get("user_role", "user")
    triggered_rule = "None"
    action = "pass"
    reason = ""

    # ✅ 模拟缓存更新（最多5条）
    if user_id not in transaction_cache:
        transaction_cache[user_id] = []
    transaction_cache[user_id].append({
        "tx_id": txn["tx_id"],
        "timestamp": datetime.utcnow().isoformat(),
        "amount": txn["amount"]
    })
    transaction_cache[user_id] = transaction_cache[user_id][-5:]  # 保留最近5条

    # 决策逻辑（含 override）
    if user_role == "reviewer":
        action = "override"
        triggered_rule = "N/A"
        reason = "Reviewer override"
    elif blackboard.risk_score > 0.85 and blackboard.transaction_country != "US":
        action = "block"
        triggered_rule = "HighRisk+Foreign"
        reason = "Risk > 0.85 & Foreign TX"
    elif blackboard.is_pep and blackboard.amount > 10000:
        action = "flag"
        triggered_rule = "PEP+LargeTX"
        reason = "PEP & Amount > 10,000"
    elif len(transaction_cache[user_id]) >= 5:
        action = "block"
        triggered_rule = "HighFreqTX"
        reason = "Too many transactions in short time"

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "tx_id": txn["tx_id"],
        "risk_score": blackboard.risk_score,
        "transaction_country": blackboard.transaction_country,
        "amount": blackboard.amount,
        "is_pep": blackboard.is_pep,
        "user_role": user_role,
        "action": action,
        "rule_triggered": triggered_rule,
        "reason": reason
    }

if __name__ == "__main__":
    # 构建行为树
    tree, blackboard = build_behavior_tree()

    # ✅ 样本交易（包含 reviewer 和频繁交易用户）
    sample_txns = [
        {"user_id": "u001", "tx_id": "txn1001", "risk_score": 0.9, "transaction_country": "CN", "amount": 12000, "is_pep": False, "user_role": "user"},
        {"user_id": "u002", "tx_id": "txn1002", "risk_score": 0.3, "transaction_country": "US", "amount": 15000, "is_pep": True, "user_role": "reviewer"},
        {"user_id": "u003", "tx_id": "txn1003", "risk_score": 0.1, "transaction_country": "US", "amount": 500, "is_pep": False, "user_role": "user"},
        {"user_id": "u003", "tx_id": "txn1004", "risk_score": 0.1, "transaction_country": "US", "amount": 600, "is_pep": False, "user_role": "user"},
        {"user_id": "u003", "tx_id": "txn1005", "risk_score": 0.1, "transaction_country": "US", "amount": 700, "is_pep": False, "user_role": "user"},
        {"user_id": "u003", "tx_id": "txn1006", "risk_score": 0.1, "transaction_country": "US", "amount": 800, "is_pep": False, "user_role": "user"},
        {"user_id": "u003", "tx_id": "txn1007", "risk_score": 0.1, "transaction_country": "US", "amount": 900, "is_pep": False, "user_role": "user"}
    ]

    logs = []
    for txn in sample_txns:
        log = run_agent_on_transaction(txn, tree, blackboard)
        print(f"[{log['tx_id']}] → {log['action']} (Rule: {log['rule_triggered']}, Role: {log['user_role']})")
        logs.append(log)

    # 写入日志文件
    with open("logs/decision_log.json", "w") as f:
        json.dump(logs, f, indent=2)
