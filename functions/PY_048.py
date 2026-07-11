def get_fk_many_from_list(
            self, object_list, fkmany, fkmany_class, key_attr):
        """Update ORM one-to-many list from object list

        Used for syncing metrics and columns using the same code"""

        object_dict = {o.get(key_attr): o for o in object_list}
        object_keys = [o.get(key_attr) for o in object_list]

        # delete fks that have been removed
        fkmany = [o for o in fkmany if getattr(o, key_attr) in object_keys]

        # sync existing fks
        for fk in fkmany:
            obj = object_dict.get(getattr(fk, key_attr))
            for attr in fkmany_class.update_from_object_fields:
                setattr(fk, attr, obj.get(attr))

        # create new fks
        new_fks = []
        orm_keys = [getattr(o, key_attr) for o in fkmany]
        for obj in object_list:
            key = obj.get(key_attr)
            if key not in orm_keys:
                del obj['id']
                orm_kwargs = {}
                for k in obj:
                    if (
                        k in fkmany_class.update_from_object_fields and
                        k in obj
                    ):
                        orm_kwargs[k] = obj[k]
                new_obj = fkmany_class(**orm_kwargs)
                new_fks.append(new_obj)
        fkmany += new_fks
        return fkmany