class Body:
    def __init__(self, head=None, body=None, arms=None, legs=None):
        self.head=head
        self.body=body
        self.arms=arms
        self.legs=legs
        
class Humanoid(Body):
    def __init__(self, head=None, body=None, arms=None, legs=None):
        super().__init__(head, body, arms, legs):
        self.neck=None
        self.hand_left=None
        self.hand_right=None
        self.waist=None
        self.feet=None

