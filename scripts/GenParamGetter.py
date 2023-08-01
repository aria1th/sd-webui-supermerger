import gradio as gr
import scripts.utils.components as components
from scripts.mergers.mergers import smergegen, simggen
from scripts.mergers.xyplot import numanager
from modules import scripts, script_callbacks

class GenParamGetter(scripts.Script):
    txt2img_gen_button = None
    img2img_gen_button = None

    txt2img_params = []
    img2img_params = []

    def title(self):
        return "Super Marger Generation Parameter Getter"
    
    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def after_component(self, component: gr.components.Component, **_kwargs):
        """Find generate button"""
        if component.elem_id == "txt2img_generate":
            GenParamGetter.txt2img_gen_button = component
        elif  component.elem_id == "img2img_generate":
            GenParamGetter.img2img_gen_button = component

    def get_components_by_ids(root: gr.Blocks, ids: list[int]):
        components: list[gr.Blocks] = []

        if root._id in ids:
            components.append(root)
            ids = [_id for _id in ids if _id != root._id]

        if isinstance(root, gr.components.BlockContext):
            for block in root.children:
                components.extend(GenParamGetter.get_components_by_ids(block, ids))

        return components
    
    def compare_components_with_ids(components: list[gr.Blocks], ids: list[int]):
        return len(components) == len(ids) and all(component._id == _id for component, _id in zip(components, ids))

    def get_params_components(demo: gr.Blocks, app):
        for _id, _is_txt2img in zip([GenParamGetter.txt2img_gen_button._id, GenParamGetter.img2img_gen_button._id], [True, False]):
            dependencies: list[dict] = [x for x in demo.dependencies if x["trigger"] == "click" and _id in x["targets"]]
            dependency: dict = None
            cnet_dependency: dict = None
            UiControlNetUnit = None
            for d in dependencies:
                if len(d["outputs"]) == 1:
                    outputs = outputs = GenParamGetter.get_components_by_ids(demo, d["outputs"])
                    output = outputs[0]
                    if (
                        isinstance(output, gr.State)
                        and type(output.value).__name__ == "UiControlNetUnit"
                    ):
                        cnet_dependency = d
                        UiControlNetUnit = type(output.value)

                elif len(d["outputs"]) == 4:
                    dependency = d

            params = [params for params in demo.fns if GenParamGetter.compare_components_with_ids(params.inputs, dependency["inputs"])]

            if _is_txt2img:
                GenParamGetter.txt2img_params = params[0].inputs
            else:
                GenParamGetter.img2img_params = params[0].inputs
        
        with demo:
            components.merge.click(
                fn=smergegen,
                inputs=[*components.msettings,components.esettings1,*components.genparams,*components.lucks,components.currentmodel,components.dfalse,*GenParamGetter.txt2img_params],
                outputs=[components.submit_result,components.currentmodel]
            )

            components.mergeandgen.click(
                fn=smergegen,
                inputs=[*components.msettings,components.esettings1,*components.genparams,*components.lucks,components.currentmodel,components.dtrue,*GenParamGetter.txt2img_params],
                outputs=[components.submit_result,components.currentmodel,*components.imagegal]
            )

            components.gen.click(
                fn=simggen,
                inputs=[*GenParamGetter.txt2img_params,components.currentmodel,components.id_sets],
                outputs=[*components.imagegal],
            )

            components.s_reserve.click(
                fn=numanager,
                inputs=[gr.Textbox(value="reserve",visible=False),*components.xysettings,*components.msettings,*components.genparams,*components.lucks,*GenParamGetter.txt2img_params],
                outputs=[components.numaframe]
            )

            components.s_reserve1.click(
                fn=numanager,
                inputs=[gr.Textbox(value="reserve",visible=False),*components.xysettings,*components.msettings,*components.genparams,*components.lucks,*GenParamGetter.txt2img_params],
                outputs=[components.numaframe]
            )

            components.gengrid.click(
                fn=numanager,
                inputs=[gr.Textbox(value="normal",visible=False),*components.xysettings,*components.msettings,*components.genparams,*components.lucks,*GenParamGetter.txt2img_params],
                outputs=[components.submit_result,components.currentmodel,*components.imagegal],
            )

            components.s_startreserve.click(
                fn=numanager,
                inputs=[gr.Textbox(value=" ",visible=False),*components.xysettings,*components.msettings,*components.genparams,*components.lucks,*GenParamGetter.txt2img_params],
                outputs=[components.submit_result,components.currentmodel,*components.imagegal],
            )

            components.rand_merge.click(
                fn=numanager,
                inputs=[gr.Textbox(value="random",visible=False),*components.xysettings,*components.msettings,*components.genparams,*components.lucks,*GenParamGetter.txt2img_params],
                outputs=[components.submit_result,components.currentmodel,*components.imagegal],
            )

script_callbacks.on_app_started(GenParamGetter.get_params_components)