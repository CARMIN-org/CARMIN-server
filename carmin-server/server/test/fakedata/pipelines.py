from server.resources.models.pipeline import Pipeline, PipelineParameter
from server.resources.models.error_code_and_message import ErrorCodeAndMessage

NameStudyOne = "study_one"
NameStudyTwo = "study_two"

PropNameOne = "prop_one"
PropNameTwo = "prop_two"

PropValueOne = "prop_value_one"
PropValueTwo = "prop_value_two"
PropValueThree = "prop_value_three"

PipelineParamOne = PipelineParameter(
    name="PipelineParam1",
    parameter_type="File",
    is_optional=False,
    is_returned_value=True,
    description="PipelineParam1 Description")

PipelineParamTwo = PipelineParameter(
    name="PipelineParam2",
    parameter_type="String",
    is_optional=False,
    is_returned_value=True,
    description="PipelineParam2 Description")

PipelineParamThree = PipelineParameter(
    name="file_input",
    parameter_type="File",
    is_optional=False,
    is_returned_value=False,
    description="PipelineParamThree description")

PipelineOne = Pipeline(
    identifier="one",
    name="one_name",
    version="version-1",
    description="One description",
    can_execute=True,
    parameters=list([PipelineParamOne]),
    properties={PropNameOne: PropValueOne},
    error_codes_and_messages=list([ErrorCodeAndMessage(1000, "Test message")]))

PipelineTwo = Pipeline(
    identifier="two",
    name="two_name",
    version="version-1",
    description="Two description",
    can_execute=False,
    parameters=list([PipelineParamOne, PipelineParamTwo]),
    properties={PropNameTwo: PropValueOne},
    error_codes_and_messages=list([ErrorCodeAndMessage(1000, "Test message")]))

PipelineThree = Pipeline(
    identifier="three",
    name="three_name",
    version="version-3",
    description="Three description",
    can_execute=True,
    parameters=list([PipelineParamOne, PipelineParamTwo]),
    properties={PropNameOne: PropValueTwo,
                PropNameTwo: PropValueThree},
    error_codes_and_messages=list(
        [ErrorCodeAndMessage(2000, "Pipeline three error code and message")]))

PIPELINE_FOUR = Pipeline(
    identifier="pipeline1",
    name="pipeline1",
    version="4.0.0",
    description="test pipeline",
    can_execute=True,
    parameters=list([PipelineParamThree]),
    properties={PropNameOne: PropValueTwo,
                PropNameTwo: PropValueThree},
    error_codes_and_messages=list(
        [ErrorCodeAndMessage(2000, "Pipeline four error code and message")]))
