from rules import Rules

r = Rules()
r.on_add("test", "test")
r.on_add("test2", "test2")
r.on_remove("test3")
print(r.Rules)