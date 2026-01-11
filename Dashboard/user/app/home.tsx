import { Redirect } from 'expo-router';

export default function Index() {
  // This forces the app to look at the _layout.tsx logic
  // and redirect the user to the correct starting screen.
  return <Redirect href="/signIn" />;
}