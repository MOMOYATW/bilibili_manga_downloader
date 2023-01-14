import TaskSets from "../components/TaskSets";

const Pending = () => {
  return (
    <TaskSets taskType="PendingList" operateName="delete" pageTitle="队列中" />
  );
};

export default Pending;
