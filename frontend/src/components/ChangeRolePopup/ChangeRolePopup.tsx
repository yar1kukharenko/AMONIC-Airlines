import React, { useState } from "react";
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  FormControl,
  FormControlLabel,
  FormLabel,
  Radio,
  RadioGroup,
  Stack,
} from "@mui/material";
import api from "@/axiosInstance";

interface ChangeRolePopupProps {
  onClose: () => void;
  open: boolean;
  role: "User" | "Administrator" | "No Role";
  id: number;
}

const ChangeRolePopup: React.FC<ChangeRolePopupProps> = ({
  onClose,
  open,
  role,
  id,
}) => {
  const [selectedRole, setSelectedRole] = useState(role);

  const editRole = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await api.put(`/user/edit-role/${id}/`, {
      role: selectedRole,
    });
    console.log(res.data);
  };

  return (
    <Dialog open={open}>
      <DialogTitle>Изменить роль</DialogTitle>
      <form onSubmit={editRole}>
        <Box sx={{ padding: 2 }}>
          <FormControl>
            <Stack spacing={2}>
              <FormLabel id="demo-radio-buttons-group-label">Роль:</FormLabel>
              <RadioGroup
                aria-labelledby="demo-radio-buttons-group-label"
                defaultValue={role}
                name="radio-buttons-group"
              >
                <FormControlLabel
                  value="Administrator"
                  control={<Radio />}
                  label="Администратор"
                  onClick={() => setSelectedRole("Administrator")}
                />
                <FormControlLabel
                  value="User"
                  control={<Radio />}
                  label="Пользователь"
                  onClick={() => setSelectedRole("User")}
                />
              </RadioGroup>
              <Stack direction="row" spacing={2}>
                <Button
                  disabled={role === selectedRole || selectedRole === "No Role"}
                  type={"submit"}
                >
                  Изменить
                </Button>
                <Button type={"submit"} onClick={onClose}>
                  Отмена
                </Button>
              </Stack>
            </Stack>
          </FormControl>
        </Box>
      </form>
    </Dialog>
  );
};

export default ChangeRolePopup;
