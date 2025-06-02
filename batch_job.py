import json
from datetime import datetime
from decision_logic import build_behavior_tree
import py_trees

def run_batch_processing(transactions):
    tree, blackboard = build_behavior_tree()
    logs = []

    for txn in transactions:
        blackboard.risk_score = txn["risk_score"]
        blackboard.transaction_country = txn["transaction_country"]
        blackboard.amount = txn["amount"]
        blackboard.is_pep = txn["is_pep"]

        bt = py_trees.trees.BehaviourTree(tree)
        bt.tick()

        action = "pass"
        if blackboard.risk_score > 0.85 and blackboard.transaction_country != "US":
            action = "block"
        elif blackboard.is_pep and blackboard.amount > 10000:
            action = "flag"

        logs.append({
            "timestamp": datetime.utcnow().isoformat(),
            "tx_id": txn["tx_id"],
            "user_id": txn["user_id"],
            "action": action
        })

    with open("logs/batch_log.json", "w") as f:
        json.dump(logs, f, indent=2)

if __name__ == "__main__":
    # 模拟交易数据
    transactions = [
        {"tx_id": "txn1", "user_id": "u1", "risk_score": 0.9, "transaction_country": "CN", "amount": 15000, "is_pep": False},
        {"tx_id": "txn2", "user_id": "u2", "risk_score": 0.3, "transaction_country": "US", "amount": 12000, "is_pep": True}
    ]
    run_batch_processing(transactions)
