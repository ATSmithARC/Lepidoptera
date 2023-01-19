using System.Collections.Generic;
using Lepidoptera_GHA.Properties;

namespace Lepidoptera_GHA
{
    public class StadiumToolsCategoryIcon : Grasshopper.Kernel.GH_AssemblyPriority
    {
        public override Grasshopper.Kernel.GH_LoadingInstruction PriorityLoad()
        {
            Grasshopper.Instances.ComponentServer.AddCategoryIcon("Lepidoptera", Resources.Lepidoptera);
            Grasshopper.Instances.ComponentServer.AddCategorySymbolName("Lepidoptera", 'L');
            return Grasshopper.Kernel.GH_LoadingInstruction.Proceed;
        }
    }
}
