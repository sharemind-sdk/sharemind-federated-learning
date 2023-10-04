import common as cm


def based10(i: int):
    if (i < 10):
        return f"0{i}"
    return f"{i}"


def generate_conf(num_clients, num_layers, filenames):
    clients = " ".join([f"Client{j}" for j in range(1, num_clients + 1)])

    for filename in filenames:
        with open(filename, "w") as f:
            # Define the usernames (Client1, Client2, Client3)
            for i in range(1, num_clients + 1):
                f.write(f"[User Client{i}]\n")
                f.write(f"TlsPublicKeyFile = %{{CurrentFileDirectory}}/keys/client{i}-pub-key\n")
            f.write("\n")

            scripts = ["import-script.sb", "main.sb", "init.sb", "global.sb", "agg.sb"]

            # Generate rulesets for sharemind:server
            f.write("[Ruleset sharemind:server]\n")
            for script in scripts:
                f.write(f"execute:{script} = {clients}\n")
            f.write("\n")

            # Generate rulesets for sharemind:tabledb
            f.write("[Ruleset sharemind:tabledb]\n")
            for script in scripts:
                f.write(f"*:{script} = {clients}\n")
            f.write("\n")

            g_models = ["init", "agg"]
            for g_model in g_models:
                for i in range(nlayers):
                    f.write(f"DS1:{g_model}.layer-{based10(i)}:*:* = {clients}\n")
                f.write("\n")

            for c in range(1, nclients + 1):
                for i in range(nlayers):
                    f.write(f"DS1:client{c}.layer-{based10(i)}:*:import-script.sb = Client{c}\n")
                f.write("\n")

            for c in range(1, nclients + 1):
                for i in range(nlayers):
                    f.write(f"DS1:client{c}.layer-{based10(i)}:read:* = {clients}\n")
                f.write("\n")


if __name__ == "__main__":
    nclients = cm.CFG["NUMBER_CLIENTS"]

    # Open the file and read its content
    with open(f"{cm.PROJECT_PATH}/client/model.txt", 'r') as file:
        content = file.read()

    # Count the number of | characters
    nlayers = content.count('|') + 1

    filenames = [
        f"{cm.PROJECT_PATH}/server/server1/access-control.conf",
        f"{cm.PROJECT_PATH}/server/server2/access-control.conf",
        f"{cm.PROJECT_PATH}/server/server3/access-control.conf"
    ]

    generate_conf(nclients, nlayers, filenames)
    print("3 access-control.conf are generated and saved!")
