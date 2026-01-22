from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class RoleName(str, Enum): 
    ADMIN = "Admin" 
    MEMBER = "Member" 


@dataclass 
class Role:
    role_id: int 
    role_name: RoleName

    def __validate(self) -> None: 
        self.__validate() 

    def _validate(self) -> None: 
        if not isinstance(self.role_id, int) or self.role_id <= 0: 
            raise ValueError("role_id phải là số nguyên dương (>0).") 
        
        if not isinstance(self.role_name, RoleName): 
            raise TypeError("role_name phải thuộc enum RoleName.")
    def is_admin(self) -> bool: 
        return self.role_name == RoleName.MEMBER
    
    def to_dict(self) -> dict: 
        return{ 
            "role_id": self.role_id, 
            "role_name": self.role_name.value
        }