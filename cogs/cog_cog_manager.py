from discord.ext import commands
import importlib
from os import getcwd

class CogManagerCog(commands.Cog):
    def __init__(self, client, *args):
        self.cogs_classes = {}
        print(f"CogManagerCog >>> Discovering Cogs")
        #iterate through args, accept the cogs that are valid and ignore invalid cogs
        for arg in args:
            #get the file and class name
            module_name = arg[0]
            cog_name = arg[1]
            cog_init_args = arg[2]

            #see if the file exists and if it has the cog
            try:
                #try to open it
                cog_module = importlib.import_module(module_name)
                #success, try to access the class now
                cog_class = getattr(cog_module, cog_name)
                #success! store the module and class
                self.cogs_classes[module_name] = (cog_class, cog_init_args)
                print(f"\tCog: {module_name}.{cog_name} [Valid]")

            except ImportError as e:
                #oops, file not found. oh well, ignore the cog
                print(f"\tCog: {module_name}.{cog_name} [Invalid: file not found]")
                print(e)
            except AttributeError as e:
                #oops, cog not found. oh well, ignore the cog
                print(f"\tCog: {module_name}.{cog_name} [Invalid: Cog not present in file]")
                print(e)
        print(f"CogManagerCog >>> Valid Cogs Found: {len(self.cogs_classes)}")

        #add cogs to bot
        self.cog_instances = {}
        for module_name, cog_class_args in self.cogs_classes.items():
            print(f"\tCog: {module_name}::{cog_class} Initializing")
            cog_class = cog_class_args[0]
            cog_args = cog_class_args[1]

            #create instance of cog
            cog_instance = cog_class(*cog_args)
            #add cog to bot
            client.add_cog(cog_instance)
            #store instance of cog
            self.cog_instances[cog_class.__name__] = cog_instance

    #yields a cog if it is an instance of SetupCog
    def get_cogs_with_setup(self):
        for cog in self.cog_instances.items():
            if isinstance(cog, SetupCog):
                yield cog

    @commands.group(pass_context=True, invoke_without_command=True)
    async def managecogs(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("<@521285684271513601> Implement a help message system already you lazy bitch")

    @managecogs.command()
    async def list(self, ctx):
        await ctx.send()
