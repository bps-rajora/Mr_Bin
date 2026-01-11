import React, { useEffect } from "react";
import { router, Slot, useSegments } from "expo-router";
import { AuthContextProvider, useAuth } from "../context/authContext";

const MainLayout = () => {
  const { isAuthenticated } = useAuth();
  const segments = useSegments();

  useEffect(() => {
    // 1. Wait for auth state to be loaded
    if (typeof isAuthenticated === "undefined") return;

    // 2. Check if user is inside the protected "(app)" group
    const inAppGroup = segments[0] === "(app)";

    if (isAuthenticated && !inAppGroup) {
      // User is logged in but NOT in the app group -> Send to home
      // Note: We use "/home" because (app) is a hidden group
      router.replace("/home"); 
    } else if (!isAuthenticated && inAppGroup) {
      // User is NOT logged in but trying to access app screens -> Send to login
      router.replace("/signIn");
    }
  }, [isAuthenticated, segments]);

  return <Slot />;
};

export default function RootLayout() {
  return (
    <AuthContextProvider>
      <MainLayout />
    </AuthContextProvider>
  );
}