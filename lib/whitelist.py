import json, hashlib, os



class MinecraftWhitelist:
    def __init__(self, file_path="whitelist.json"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file)

    def load_whitelist(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_whitelist(self, data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def add_player(self, name):
        whitelist = self.load_whitelist()
        uuid = self.generate_offline_uuid(name)

        if any(player["uuid"] == uuid for player in whitelist):
            print(f"Игрок с UUID {uuid} уже в белом списке.")
            return

        whitelist.append({"uuid": uuid, "name": name})
        self.save_whitelist(whitelist)

    def remove_player(self, name):
        whitelist = self.load_whitelist()

        new_whitelist = [player for player in whitelist if player["name"] != name]
        if len(new_whitelist) == len(whitelist):
            return
        self.save_whitelist(new_whitelist)

    def list_players(self):
        whitelist = self.load_whitelist()
        if not whitelist:
            print("Белый список пуст.")
            return
        print("Игроки в белом списке:")
        for player in whitelist:
            print(f"{player['name']}: {player['uuid']}")


    def generate_offline_uuid(self, name):
        input_str = f'OfflinePlayer:{name}'
        hash_md5 = hashlib.md5(input_str.encode()).digest()

        byte_array = list(hash_md5)

        byte_array[6] = (byte_array[6] & 0x0F) | 0x30 
        byte_array[8] = (byte_array[8] & 0x3F) | 0x80  

        uuid_hex = ''.join(f'{byte:02x}' for byte in byte_array)
        return self.split_uuid(uuid_hex)

    def split_uuid(self, uuid_hex):
        return '-'.join([
            uuid_hex[0:8],
            uuid_hex[8:12],
            uuid_hex[12:16],
            uuid_hex[16:20],
            uuid_hex[20:32],
        ])






if __name__ == "__main__":
    whitelist_manager = MinecraftWhitelist()
    whitelist_manager.add_player("_Dallix_")