from dungeon_life_agent.pipelines import AssetPipelineNavigator


def test_pipeline_navigator_describes_pipeline():
    navigator = AssetPipelineNavigator()
    names = list(navigator.available())
    assert "blender" in names

    description = navigator.get("react_ts").describe()
    assert "React/TypeScript" in description
    assert "Storybook" in description
