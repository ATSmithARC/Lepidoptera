using Grasshopper;
using Grasshopper.Kernel;
using System;
using System.Drawing;
using System.Resources;
using Lepidoptera_GHA.Properties;

namespace Lepidoptera_GHA
{
    public class Lepidoptera_GHAInfo : GH_AssemblyInfo
    {
        public override string Name => "Lepidoptera";

        //Return a 24x24 pixel bitmap to represent this GHA library.
        public override Bitmap Icon => Resources.Lepidoptera;

        //Return a short string describing the purpose of this GHA library.
        public override string Description => "";

        public override Guid Id => new Guid("45f7169e-940f-4fc7-9e60-41ea93474133");

        //Return a string identifying you or your company.
        public override string AuthorName => "";

        //Return a string representing your preferred contact details.
        public override string AuthorContact => "";
    }
}