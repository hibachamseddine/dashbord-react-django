import json
from channels.generic.websocket import AsyncWebsocketConsumer

class EmployeeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("employees", self.channel_name)
        await self.accept()
        print("✅ WebSocket connecté !")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("employees", self.channel_name)
        print("❌ WebSocket déconnecté.")

    async def broadcast_employee(self, event):
        """🔄 Rafraîchir les employés en temps réel"""
        await self.send(text_data=json.dumps({
            "type": "update",
            "message": event.get("message", "Nouvel employé ajouté !"),
            
            
        }))
        
        
    async def broadcast_employee_deleted(self, event):
        """🗑️ Notifier la suppression d'un employé"""
        print(f"🔴 WebSocket envoie suppression: {event}")  # Debug
        await self.send(text_data=json.dumps({
            "type": "delete",  # "delete" pour la suppression
            "employee_id": event.get("employee_id"),  # ✅ Vérifie ici !
            "message": event.get("message", "Un employé a été supprimé."),
        }))





class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("projects", self.channel_name)
        await self.accept()
        print("✅ WebSocket connecté !")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("projects", self.channel_name)
        print("❌ WebSocket déconnecté.")

    async def broadcast_project(self, event):
        
        await self.send(text_data=json.dumps({
            "type": "update",
            "message": event.get("message", "Nouvel project ajouté !"),
        }))
        
    async def broadcast_project_deleted(self, event):
        """🗑️ Notifier la suppression d'un employé"""
        print(f"🔴 WebSocket envoie suppression: {event}")  # Debug
        await self.send(text_data=json.dumps({
            "type": "delete",  # "delete" pour la suppression
            "project_id": event.get("project_id"),  # ✅ Vérifie ici !
            "message": event.get("message", "Un project a été supprimé."),
        }))

