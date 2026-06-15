"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Loader2 } from "lucide-react";

import { PageHeader } from "@/components/dashboard/page-header";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuthStore } from "@/lib/stores/auth-store";
import { useChangePassword, useUpdateProfile } from "@/lib/hooks/use-user";
import { initials } from "@/lib/utils";

export default function ProfilePage() {
  const user = useAuthStore((s) => s.user);
  const updateProfile = useUpdateProfile();
  const changePassword = useChangePassword();

  const profileForm = useForm({
    defaultValues: { full_name: "", headline: "", avatar_url: "" },
  });
  const passwordForm = useForm({
    defaultValues: { current_password: "", new_password: "" },
  });

  useEffect(() => {
    if (user) {
      profileForm.reset({
        full_name: user.full_name ?? "",
        headline: user.headline ?? "",
        avatar_url: user.avatar_url ?? "",
      });
    }
  }, [user, profileForm]);

  return (
    <div>
      <PageHeader title="Profile" description="Manage your personal information and password." />

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Personal information</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="mb-6 flex items-center gap-4">
              <Avatar className="size-16 text-lg">
                {user?.avatar_url && <AvatarImage src={user.avatar_url} />}
                <AvatarFallback>{initials(user?.full_name)}</AvatarFallback>
              </Avatar>
              <div>
                <p className="font-medium">{user?.full_name}</p>
                <p className="text-sm text-muted-foreground">{user?.email}</p>
              </div>
            </div>

            <form
              onSubmit={profileForm.handleSubmit((values) => updateProfile.mutate(values))}
              className="space-y-4"
            >
              <div className="space-y-2">
                <Label htmlFor="full_name">Full name</Label>
                <Input id="full_name" {...profileForm.register("full_name")} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="headline">Headline</Label>
                <Input id="headline" placeholder="Senior Full Stack Engineer" {...profileForm.register("headline")} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="avatar_url">Avatar URL</Label>
                <Input id="avatar_url" placeholder="https://…" {...profileForm.register("avatar_url")} />
              </div>
              <Button type="submit" disabled={updateProfile.isPending}>
                {updateProfile.isPending && <Loader2 className="animate-spin" />}
                Save changes
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Change password</CardTitle>
          </CardHeader>
          <CardContent>
            <form
              onSubmit={passwordForm.handleSubmit((values) =>
                changePassword.mutate(values, { onSuccess: () => passwordForm.reset() })
              )}
              className="space-y-4"
            >
              <div className="space-y-2">
                <Label htmlFor="current_password">Current password</Label>
                <Input id="current_password" type="password" {...passwordForm.register("current_password")} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="new_password">New password</Label>
                <Input id="new_password" type="password" {...passwordForm.register("new_password")} />
                <p className="text-xs text-muted-foreground">
                  Min 8 chars with uppercase, lowercase and a number.
                </p>
              </div>
              <Button type="submit" variant="outline" disabled={changePassword.isPending}>
                {changePassword.isPending && <Loader2 className="animate-spin" />}
                Update password
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
