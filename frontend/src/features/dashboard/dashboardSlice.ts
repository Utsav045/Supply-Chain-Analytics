import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { getDashboardSummary } from "./dashboardService";
import type { DashboardSummary } from "./types";

interface DashboardState {
  data: DashboardSummary | null;
  loading: boolean;
  error: string | null;
}

const initialState: DashboardState = {
  data: null,
  loading: false,
  error: null,
};

export const fetchDashboardData = createAsyncThunk(
  "dashboard/fetchDashboardData",
  async () => {
    const data = await getDashboardSummary();
    return data;
  },
);

const dashboardSlice = createSlice({
  name: "dashboard",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchDashboardData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })

      .addCase(fetchDashboardData.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })

      .addCase(fetchDashboardData.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.error.message || "Failed to load dashboard data.";
      });
  },
});

export default dashboardSlice.reducer;