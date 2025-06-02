import py_trees

class RiskScoreCheck(py_trees.behaviour.Behaviour):
    def __init__(self, threshold):
        super().__init__(name=f"Risk > {threshold}")
        self.threshold = threshold

    def update(self):
        risk_score = self.blackboard.get("risk_score")
        if risk_score is not None and risk_score > self.threshold:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE

class CountryCheck(py_trees.behaviour.Behaviour):
    def __init__(self, not_country):
        super().__init__(name=f"Not {not_country}")
        self.not_country = not_country

    def update(self):
        country = self.blackboard.get("transaction_country")
        if country and country != self.not_country:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE

class AmountCheck(py_trees.behaviour.Behaviour):
    def __init__(self, min_amount):
        super().__init__(name=f"Amount > {min_amount}")
        self.min_amount = min_amount

    def update(self):
        amount = self.blackboard.get("amount")
        if amount is not None and amount > self.min_amount:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE

class IsPEPCheck(py_trees.behaviour.Behaviour):
    def __init__(self):
        super().__init__(name="Is PEP")

    def update(self):
        is_pep = self.blackboard.get("is_pep")
        if is_pep is True:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE

class FlagAction(py_trees.behaviour.Behaviour):
    def __init__(self):
        super().__init__(name="Flag TX")

    def update(self):
        print("🔔 Flagged transaction for review.")
        return py_trees.common.Status.SUCCESS

class BlockAction(py_trees.behaviour.Behaviour):
    def __init__(self):
        super().__init__(name="Block TX")

    def update(self):
        print("⛔ Blocked transaction.")
        return py_trees.common.Status.SUCCESS

def build_behavior_tree():
    blackboard = py_trees.blackboard.Client(name="AML Blackboard")
    blackboard.register_key(key="risk_score", access=py_trees.common.Access.READ)
    blackboard.register_key(key="risk_score", access=py_trees.common.Access.WRITE)
    blackboard.register_key(key="transaction_country", access=py_trees.common.Access.READ)
    blackboard.register_key(key="transaction_country", access=py_trees.common.Access.WRITE)
    blackboard.register_key(key="amount", access=py_trees.common.Access.READ)
    blackboard.register_key(key="amount", access=py_trees.common.Access.WRITE)
    blackboard.register_key(key="is_pep", access=py_trees.common.Access.READ)
    blackboard.register_key(key="is_pep", access=py_trees.common.Access.WRITE)

    # 创建行为节点
    risk_check = RiskScoreCheck(0.85)
    country_check = CountryCheck("US")
    block = BlockAction()

    pep_check = IsPEPCheck()
    amount_check = AmountCheck(10000)
    flag = FlagAction()

    # ✅ 挂载 blackboard
    for node in [risk_check, country_check, block, pep_check, amount_check, flag]:
        node.blackboard = blackboard

    # 行为树结构
    high_risk_seq = py_trees.composites.Sequence(name = "HighRisk+Foreign", memory=False)
    high_risk_seq.add_children([risk_check, country_check, block])

    pep_seq = py_trees.composites.Sequence(name = "PEP+LargeTX", memory=False)
    pep_seq.add_children([pep_check, amount_check, flag])

    root = py_trees.composites.Selector(name = "AML Root", memory=False)
    root.add_children([high_risk_seq, pep_seq])

    return root, blackboard

if __name__ == "__main__":
    tree, blackboard = build_behavior_tree()
    blackboard.risk_score = 0.9
    blackboard.transaction_country = "CN"
    blackboard.amount = 20000
    blackboard.is_pep = False

    bt = py_trees.trees.BehaviourTree(root=tree)
    bt.tick()

    py_trees.display.render_dot_tree(bt.root, name="aml_behavior_tree")
